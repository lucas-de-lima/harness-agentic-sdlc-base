from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import json as _json

from .github_identity import preflight_github


# Exposed for testing — tests can mock this to avoid calling the actual `gh` CLI
_gh_run = subprocess.run


MERGE_TYPE_MAP: dict[str, tuple[str, str, str]] = {
    "story_to_feature": (
        "HG-MERGE-STORY",
        "story/<name> -> feature/<name>",
        "Merge story branch into its parent feature branch.",
    ),
    "feature_to_develop": (
        "HG-MERGE-FEATURE",
        "feature/<name> -> develop",
        "Merge completed feature into the develop integration branch.",
    ),
    "develop_to_main": (
        "HG-MERGE-DEVELOP",
        "develop -> main",
        "Merge develop into main for release.",
    ),
}


@dataclass
class MergeResult:
    ok: bool
    gate_id: str | None = None
    merge_type: str | None = None
    affected_object: str | None = None
    pr_number: int | None = None
    sha: str | None = None
    merged: bool = False
    error: str | None = None
    evidence: dict | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def _gates_file(root: Path) -> Path:
    return root / ".harness" / "hitl" / "gates.json"


def _find_approved_gate(gates: list[dict], gate_id: str, affected_object: str) -> dict | None:
    for g in gates:
        if (
            g.get("gate_id") == gate_id
            and g.get("affected_object") == affected_object
            and g.get("state") == "approved"
        ):
            return g
    return None


def controlled_merge(
    root: Path,
    merge_type: str,
    affected_object: str,
    pr_number: int,
    owner: str | None = None,
    repo: str | None = None,
) -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()

    # 1. Validate merge type
    gate_info = MERGE_TYPE_MAP.get(merge_type)
    if not gate_info:
        return MergeResult(
            ok=False, error=f"Unknown merge type '{merge_type}'. Valid: {list(MERGE_TYPE_MAP.keys())}"
        ).to_dict()

    gate_id, scope_desc, _ = gate_info

    result = MergeResult(
        ok=False,
        gate_id=gate_id,
        merge_type=merge_type,
        affected_object=affected_object,
        pr_number=pr_number,
    )

    # 2. GitHub identity preflight
    identity = preflight_github(root, expected_owner=owner, expected_repo=repo)
    if not identity.ok:
        result.error = f"Identity preflight failed: {'; '.join(identity.errors)}"
        return result.to_dict()

    gh_owner = identity.canonical_owner
    gh_repo = identity.canonical_repo

    # 3. Load gates and check for approved gate
    gates_path = _gates_file(root)
    if not gates_path.exists():
        result.error = (
            f"No HITL gate file found at {gates_path}. "
            f"Merge {merge_type} ({affected_object}) is BLOCKED. "
            f"Gate {gate_id} must be created and approved by a human first."
        )
        return result.to_dict()

    try:
        gates = json.loads(gates_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        result.error = f"Cannot read HITL gate file: {e}"
        return result.to_dict()

    approved_gate = _find_approved_gate(gates, gate_id, affected_object)
    if not approved_gate:
        result.error = (
            f"No approved {gate_id} gate found for '{affected_object}'. "
            f"Merge {merge_type} ({scope_desc}) is BLOCKED. "
            "A human must create and approve a gate first."
        )
        return result.to_dict()

    # 4. Gate is approved — check PR state before merging
    pr_check_cmd = [
        "gh", "pr", "view", str(pr_number),
        "--repo", f"{gh_owner}/{gh_repo}",
        "--json", "state,mergedAt",
    ]

    try:
        pr_check_proc = _gh_run(
            pr_check_cmd,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        result.error = "gh pr view timed out after 30s"
        return result.to_dict()
    except FileNotFoundError:
        result.error = "'gh' (GitHub CLI) not found."
        return result.to_dict()

    if pr_check_proc.returncode == 0 and pr_check_proc.stdout.strip():
        try:
            pr_data = _json.loads(pr_check_proc.stdout)
            if pr_data.get("state") == "MERGED":
                result.ok = True
                result.merged = True
                result.sha = pr_data.get("mergedAt", "unknown")
                result.evidence = {
                    "gate_id": gate_id,
                    "instance_id": approved_gate.get("instance_id"),
                    "merge_type": merge_type,
                    "affected_object": affected_object,
                    "pr_number": pr_number,
                    "owner": gh_owner,
                    "repo": gh_repo,
                    "note": "PR was already merged. No merge executed.",
                    "merge_origin": approved_gate.get("merge_origin") or "human_manual",
                }
                return result.to_dict()
        except (_json.JSONDecodeError, ValueError, TypeError):
            pass

    # 5. PR is open — execute the merge
    merge_cmd = [
        "gh", "pr", "merge", str(pr_number),
        "--repo", f"{gh_owner}/{gh_repo}",
        "--squash",
        "--subject", f"Controlled merge by harnessctl: {gate_id} ({affected_object})",
    ]

    try:
        proc = _gh_run(
            merge_cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        result.error = "gh pr merge timed out after 60s"
        return result.to_dict()
    except FileNotFoundError:
        result.error = (
            "'gh' (GitHub CLI) not found. Install it from https://cli.github.com/ "
            "to use controlled merge."
        )
        return result.to_dict()

    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        result.error = f"Merge failed: {stderr}"
        return result.to_dict()

    # 5. Record evidence
    evidence = {
        "gate_id": gate_id,
        "instance_id": approved_gate.get("instance_id"),
        "approved_by": approved_gate.get("decided_by"),
        "approved_at": approved_gate.get("decided_at"),
        "merge_type": merge_type,
        "affected_object": affected_object,
        "pr_number": pr_number,
        "owner": gh_owner,
        "repo": gh_repo,
        "merged_at": timestamp,
        "merge_origin": "harness_controlled",
        "merge_output": proc.stdout.strip(),
    }

    # Append evidence to the gate record
    for g in gates:
        if g.get("instance_id") == approved_gate.get("instance_id"):
            if g.get("merge_evidence") is None or not isinstance(g["merge_evidence"], list):
                g["merge_evidence"] = []
            g["merge_evidence"].append({
                "merge_type": merge_type,
                "pr_number": pr_number,
                "merged_at": timestamp,
            })
            g["merge_origin"] = "harness_controlled"
            break

    try:
        gates_path.parent.mkdir(parents=True, exist_ok=True)
        gates_path.write_text(json.dumps(gates, indent=2) + "\n", encoding="utf-8")
    except OSError as e:
        result.error = f"Cannot write merge evidence to gates file: {e}"
        return result.to_dict()

    result.ok = True
    result.merged = True
    result.sha = proc.stdout.strip()
    result.evidence = evidence

    return result.to_dict()