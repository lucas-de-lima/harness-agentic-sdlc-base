#!/usr/bin/env python3
"""
validate_hitl_merge.py

Scans the Git merge history of a Dedicated Harness repository and verifies that every
merge has a corresponding approved HITL gate.

Usage:
    python3 scripts/validate_hitl_merge.py <project-root>

Exit codes:
    0 — all merges compliant
    1 — one or more merges missing required gate approval
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REQUIRED_MERGE_GATES = {
    "HG-MERGE-STORY",
    "HG-MERGE-FEATURE",
    "HG-MERGE-DEVELOP",
}


def _get_merge_log(root: Path) -> list[dict]:
    """Get merge commit information from git log."""
    try:
        result = subprocess.run(
            [
                "git", "log", "--merges",
                "--format=%H|%P|%s",
                "--all",
                "-100",
            ],
            capture_output=True, text=True, timeout=30, cwd=str(root),
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []

    merges = []
    for line in result.stdout.strip().splitlines():
        parts = line.split("|", 2)
        if len(parts) == 3:
            sha, parents, subject = parts
            # Determine merge type from subject or parent count
            parent_count = len(parents.split())
            merges.append({
                "sha": sha,
                "parents": parent_count,
                "subject": subject,
            })
    return merges


def _classify_merge(merge: dict, branches: list[str]) -> str:
    """Classify a merge commit by its likely type."""
    subject = merge["subject"].lower()

    # Try to determine which branches are involved
    # Look for branch names in the subject
    for branch_name in branches:
        bl = branch_name.lower()
        if bl.startswith("feature/") and bl in subject:
            return "feature_to_develop"
        if bl.startswith("story/") and bl in subject:
            return "story_to_feature"
        if bl.startswith("hotfix/") and bl in subject:
            return "story_to_feature"

    # Heuristic fallbacks
    if merge["parents"] >= 2:
        if "to main" in subject or "into main" in subject or "→ main" in subject:
            return "develop_to_main"
        if "to develop" in subject or "into develop" in subject or "→ develop" in subject:
            return "feature_to_develop"

    return "unknown"


def _load_gates(root: Path) -> list[dict]:
    gates_file = root / ".harness" / "hitl" / "gates.json"
    if not gates_file.exists():
        return []
    try:
        data = json.loads(gates_file.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _get_approved_gate_objects(gates: list[dict], gate_id: str) -> set[str]:
    return {
        g.get("affected_object", "")
        for g in gates
        if g.get("gate_id") == gate_id and g.get("state") == "approved"
    }


def _get_local_branches(root: Path) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "branch", "--format=%(refname:short)"],
            capture_output=True, text=True, timeout=10, cwd=str(root),
        )
        return result.stdout.strip().splitlines()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return []


def validate_merges(root: Path) -> dict:
    gates = _load_gates(root)
    merges = _get_merge_log(root)
    branches = _get_local_branches(root)

    approved_story = _get_approved_gate_objects(gates, "HG-MERGE-STORY")
    approved_feature = _get_approved_gate_objects(gates, "HG-MERGE-FEATURE")
    approved_develop = _get_approved_gate_objects(gates, "HG-MERGE-DEVELOP")

    violations = []

    for merge in merges:
        merge_type = _classify_merge(merge, branches)
        if merge_type == "unknown":
            continue

        # Extract the affected object from the subject
        subject = merge["subject"]
        # Try to find the branch name in the subject
        affected_object = ""
        for b in branches:
            if b.lower() in subject.lower():
                affected_object = b
                break

        if not affected_object:
            # Use heuristic: look for feature/ story/ in subject
            for word in subject.split():
                if word.startswith(("feature/", "story/")):
                    affected_object = word
                    break

        if merge_type == "story_to_feature":
            if affected_object and affected_object not in approved_story:
                violations.append({
                    "sha": merge["sha"],
                    "merge_type": merge_type,
                    "subject": merge["subject"],
                    "affected_object": affected_object,
                    "issue": (
                        f"No approved HG-MERGE-STORY gate for '{affected_object}'. "
                        f"Story→Feature merge without human approval."
                    ),
                })
        elif merge_type == "feature_to_develop":
            if affected_object and affected_object not in approved_feature:
                violations.append({
                    "sha": merge["sha"],
                    "merge_type": merge_type,
                    "subject": merge["subject"],
                    "affected_object": affected_object,
                    "issue": (
                        f"No approved HG-MERGE-FEATURE gate for '{affected_object}'. "
                        f"Feature→develop merge without human approval."
                    ),
                })
        elif merge_type == "develop_to_main":
            if affected_object and affected_object not in approved_develop:
                violations.append({
                    "sha": merge["sha"],
                    "merge_type": merge_type,
                    "subject": merge["subject"],
                    "affected_object": affected_object,
                    "issue": (
                        f"No approved HG-MERGE-DEVELOP gate for 'develop'. "
                        f"develop→main merge without human approval."
                    ),
                })

    return {
        "valid": len(violations) == 0,
        "total_merges": len(merges),
        "violations": violations,
        "approved_gates": {
            "HG-MERGE-STORY": sorted(approved_story),
            "HG-MERGE-FEATURE": sorted(approved_feature),
            "HG-MERGE-DEVELOP": sorted(approved_develop),
        },
    }


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate_hitl_merge.py <project-root>")
        return 1

    root = Path(sys.argv[1]).resolve()
    if not root.exists():
        print(f"Path not found: {root}")
        return 1

    result = validate_merges(root)
    print(json.dumps(result, indent=2))

    if not result["valid"]:
        print(f"\nFAIL: {len(result['violations'])} merge violation(s) detected.")
        for v in result["violations"]:
            print(f"  - {v['issue']} (sha: {v['sha']})")
        return 1

    print(f"\nPASS: All {result['total_merges']} merge(s) compliant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())