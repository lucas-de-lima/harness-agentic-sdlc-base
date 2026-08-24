from __future__ import annotations

import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path


MANDATORY_GATES: set[str] = {
    "HG-PRODUCT",
    "HG-ARCHITECTURE",
    "HG-SCOPE",
    "HG-MERGE-STORY",
    "HG-MERGE-FEATURE",
    "HG-MERGE-DEVELOP",
    "HG-RELEASE",
    "HG-SECURITY-EXCEPTION",
    "HG-DESTRUCTIVE",
    "HG-DEPLOY",
}

MERGE_GATES: set[str] = {
    "HG-MERGE-STORY",
    "HG-MERGE-FEATURE",
    "HG-MERGE-DEVELOP",
}

PR_STATES = {"OPEN", "MERGED", "CLOSED"}

MERGE_ORIGINS = {"harness_controlled", "human_manual"}

RESUME_TARGETS: dict[str, str] = {
    "HG-MERGE-STORY": "story_in_progress",
    "HG-MERGE-FEATURE": "feature_in_progress",
    "HG-MERGE-DEVELOP": "develop_not_merged",
    "HG-RELEASE": "release_not_approved",
    "HG-PRODUCT": "product_decision_pending",
    "HG-ARCHITECTURE": "architecture_escalation",
    "HG-SCOPE": "scope_escalation",
    "HG-SECURITY-EXCEPTION": "security_blocked",
    "HG-DESTRUCTIVE": "destructive_blocked",
    "HG-DEPLOY": "deploy_blocked",
}


@dataclass
class GateInstance:
    gate_id: str
    instance_id: str
    workflow: str
    affected_object: str
    reason: str
    evidence: str
    state: str  # pending / approved / rejected
    expected_authority: str
    created_at: str
    decided_at: str | None = None
    decision: str | None = None  # approved / rejected
    decided_by: str | None = None
    note: str | None = None
    merge_origin: str | None = None  # "harness_controlled" | "human_manual" | None
    merge_evidence: list[dict] | None = None

    def to_dict(self) -> dict:
        return asdict(self)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _gen_instance_id() -> str:
    return f"hitl_{uuid.uuid4().hex[:12]}"


def _gates_dir(root: Path) -> Path:
    return root / ".harness" / "hitl"


def _gates_file(root: Path) -> Path:
    return _gates_dir(root) / "gates.json"


def _load_gates(root: Path) -> list[dict]:
    path = _gates_file(root)
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return []


def _save_gates(root: Path, gates: list[dict]) -> None:
    path = _gates_file(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(gates, indent=2) + "\n",
        encoding="utf-8",
    )


def _find_gate(gates: list[dict], instance_id: str) -> dict | None:
    for g in gates:
        if g.get("instance_id") == instance_id:
            return g
    return None


def _find_pending_for_object(
    gates: list[dict], gate_id: str, affected_object: str
) -> dict | None:
    for g in gates:
        if (
            g.get("gate_id") == gate_id
            and g.get("affected_object") == affected_object
            and g.get("state") == "pending"
        ):
            return g
    return None


def _find_gate_for_object(
    gates: list[dict], gate_id: str, affected_object: str
) -> dict | None:
    for g in gates:
        if (
            g.get("gate_id") == gate_id
            and g.get("affected_object") == affected_object
        ):
            return g
    return None


def create_gate(
    root: Path,
    gate_id: str,
    workflow: str,
    affected_object: str,
    reason: str,
    evidence: str,
    expected_authority: str,
) -> dict:
    if gate_id not in MANDATORY_GATES:
        return {
            "ok": False,
            "error": f"Unknown gate_id '{gate_id}'. Valid: {sorted(MANDATORY_GATES)}",
        }

    gates = _load_gates(root)
    existing = _find_pending_for_object(gates, gate_id, affected_object)
    if existing:
        return {
            "ok": False,
            "error": (
                f"A pending gate already exists for {gate_id} on "
                f"'{affected_object}': {existing['instance_id']}"
            ),
        }

    instance = GateInstance(
        gate_id=gate_id,
        instance_id=_gen_instance_id(),
        workflow=workflow,
        affected_object=affected_object,
        reason=reason,
        evidence=evidence,
        state="pending",
        expected_authority=expected_authority,
        created_at=_now_iso(),
    )

    gates.append(instance.to_dict())
    _save_gates(root, gates)

    return {
        "ok": True,
        "action": "created",
        "gate": instance.to_dict(),
        "message": (
            f"Human Gate {gate_id} created for '{affected_object}'. "
            "Workflow PAUSED. Awaiting human approval."
        ),
    }


def approve_gate(
    root: Path,
    instance_id: str,
    decided_by: str,
    note: str | None = None,
    merge_origin: str | None = None,
) -> dict:
    gates = _load_gates(root)
    gate = _find_gate(gates, instance_id)
    if not gate:
        return {"ok": False, "error": f"Gate not found: {instance_id}"}
    if gate["state"] != "pending":
        return {
            "ok": False,
            "error": f"Gate already {gate['state']}. Cannot approve.",
        }

    gate["state"] = "approved"
    gate["decision"] = "approved"
    gate["decided_at"] = _now_iso()
    gate["decided_by"] = decided_by
    if merge_origin:
        if merge_origin not in MERGE_ORIGINS:
            return {"ok": False, "error": f"Invalid merge_origin '{merge_origin}'. Valid: {sorted(MERGE_ORIGINS)}"}
        gate["merge_origin"] = merge_origin
    if note:
        gate["note"] = note

    _save_gates(root, gates)

    return {
        "ok": True,
        "action": "approved",
        "gate": gate,
        "message": (
            f"Gate {gate['gate_id']} ({instance_id}) approved by {decided_by}. "
            f"Merge origin: {merge_origin or 'not_specified'}. "
            "Workflow may continue."
        ),
    }


def reject_gate(
    root: Path,
    instance_id: str,
    decided_by: str,
    note: str | None = None,
) -> dict:
    gates = _load_gates(root)
    gate = _find_gate(gates, instance_id)
    if not gate:
        return {"ok": False, "error": f"Gate not found: {instance_id}"}
    if gate["state"] != "pending":
        return {
            "ok": False,
            "error": f"Gate already {gate['state']}. Cannot reject.",
        }

    gate["state"] = "rejected"
    gate["decision"] = "rejected"
    gate["decided_at"] = _now_iso()
    gate["decided_by"] = decided_by
    if note:
        gate["note"] = note

    _save_gates(root, gates)

    resume_target = RESUME_TARGETS.get(gate["gate_id"], "prior_state")

    return {
        "ok": True,
        "action": "rejected",
        "gate": gate,
        "resume_target": resume_target,
        "message": (
            f"Gate {gate['gate_id']} ({instance_id}) rejected by {decided_by}. "
            f"Workflow returns to: {resume_target}."
        ),
    }


def resume_check(
    root: Path,
    instance_id: str,
    pr_state: str | None = None,
) -> dict:
    gates = _load_gates(root)
    gate = _find_gate(gates, instance_id)
    if not gate:
        return {
            "ok": False,
            "can_resume": False,
            "error": f"Gate not found: {instance_id}",
        }

    if pr_state is not None and pr_state not in PR_STATES:
        return {
            "ok": False,
            "can_resume": False,
            "error": f"Invalid pr_state '{pr_state}'. Valid: {sorted(PR_STATES)}",
        }

    # PR state takes precedence over gate state when PR is already merged
    if pr_state == "MERGED":
        return {
            "ok": True,
            "can_resume": True,
            "gate": gate,
            "pr_state": "MERGED",
            "merge_origin": gate.get("merge_origin") or "human_manual",
            "message": "PR already merged. Gate considered satisfied. Workflow may continue.",
        }

    if pr_state == "CLOSED":
        return {
            "ok": True,
            "can_resume": False,
            "gate": gate,
            "pr_state": "CLOSED",
            "resume_target": RESUME_TARGETS.get(gate["gate_id"], "prior_state"),
            "message": "PR closed without merge. Workflow must return to correction state.",
        }

    if gate["state"] == "approved":
        merge_origin = gate.get("merge_origin") or "harness_controlled"
        return {
            "ok": True,
            "can_resume": True,
            "gate": gate,
            "pr_state": pr_state or "UNKNOWN",
            "merge_origin": merge_origin,
            "message": f"Gate approved (origin: {merge_origin}). Workflow may continue.",
        }
    elif gate["state"] == "rejected":
        resume_target = RESUME_TARGETS.get(gate["gate_id"], "prior_state")
        return {
            "ok": True,
            "can_resume": False,
            "gate": gate,
            "resume_target": resume_target,
            "message": (
                f"Gate rejected. Workflow returns to: {resume_target}."
            ),
        }
    else:
        return {
            "ok": True,
            "can_resume": False,
            "gate": gate,
            "pr_state": pr_state or "UNKNOWN",
            "message": "Gate pending. Workflow must stay PAUSED.",
        }


def reconcile_gate(
    root: Path,
    instance_id: str,
    pr_state: str | None = None,
    pr_number: int | None = None,
) -> dict:
    gates = _load_gates(root)
    gate = _find_gate(gates, instance_id)
    if not gate:
        return {
            "ok": False,
            "gate_found": False,
            "error": f"Gate not found: {instance_id}",
        }

    issues: list[str] = []

    gate_state = gate["state"]
    gate_merge_origin = gate.get("merge_origin")

    if pr_state == "MERGED":
        if gate_state == "pending":
            issues.append(
                f"PR is MERGED but gate is still pending. "
                "Gate will be auto-satisfied; record merge_origin."
            )
        if gate_merge_origin is None:
            issues.append(
                "PR is MERGED but no merge_origin recorded in gate. "
                "Assuming human_manual; call record_manual_merge() to update."
            )
        if gate_merge_origin == "harness_controlled" and not gate.get("merge_evidence"):
            issues.append(
                "merge_origin is 'harness_controlled' but no merge_evidence found. "
                "Evidence may be missing."
            )
    elif pr_state == "OPEN":
        if gate_state == "approved":
            issues.append(
                "PR is OPEN and gate is approved. "
                "Call controlled_merge to execute the merge."
            )
    elif pr_state == "CLOSED":
        if gate_state == "approved":
            issues.append(
                "PR is CLOSED without merge but gate was approved. "
                "Workflow must return to correction state."
            )

    return {
        "ok": len(issues) == 0,
        "gate_found": True,
        "gate": gate,
        "pr_state": pr_state,
        "issues": issues,
        "reconciled": len(issues) == 0,
        "message": "Gate and PR state reconciled." if len(issues) == 0
                   else f"Reconciliation found {len(issues)} issue(s).",
    }


def record_manual_merge(
    root: Path,
    instance_id: str,
    decided_by: str,
    pr_number: int | None = None,
    note: str | None = None,
) -> dict:
    gates = _load_gates(root)
    gate = _find_gate(gates, instance_id)
    if not gate:
        return {"ok": False, "error": f"Gate not found: {instance_id}"}

    gate["state"] = "approved"
    gate["decision"] = "approved"
    gate["merge_origin"] = "human_manual"
    gate["decided_at"] = gate.get("decided_at") or _now_iso()
    gate["decided_by"] = gate.get("decided_by") or decided_by
    if note:
        gate["note"] = note
    if gate.get("merge_evidence") is None or not isinstance(gate["merge_evidence"], list):
        gate["merge_evidence"] = []
    gate["merge_evidence"].append({
        "merge_origin": "human_manual",
        "pr_number": pr_number,
        "recorded_at": _now_iso(),
    })

    _save_gates(root, gates)

    return {
        "ok": True,
        "action": "manual_merge_recorded",
        "gate": gate,
        "message": (
            f"Manual merge recorded for {gate['gate_id']} ({instance_id}) "
            f"by {decided_by}. Gate set to approved (origin: human_manual)."
        ),
    }


def list_gates(root: Path, state_filter: str | None = None) -> dict:
    gates = _load_gates(root)
    if state_filter:
        gates = [g for g in gates if g.get("state") == state_filter]
    return {
        "ok": True,
        "total": len(gates),
        "gates": gates,
    }


def check_merge_allowed(
    root: Path,
    merge_type: str,
    affected_object: str,
    pr_state: str | None = None,
) -> dict:
    gate_map = {
        "story_to_feature": "HG-MERGE-STORY",
        "feature_to_develop": "HG-MERGE-FEATURE",
        "develop_to_main": "HG-MERGE-DEVELOP",
    }
    gate_id = gate_map.get(merge_type)
    if not gate_id:
        return {
            "ok": False,
            "allowed": False,
            "error": f"Unknown merge type: {merge_type}",
        }

    gates = _load_gates(root)
    gate = _find_gate_for_object(gates, gate_id, affected_object)

    if not gate:
        return {
            "ok": False,
            "allowed": False,
            "error": (
                f"No {gate_id} gate found for '{affected_object}'. "
                "Merge is BLOCKED. Create a gate and get human approval first."
            ),
        }

    # PR already merged → gate considered satisfied
    if pr_state == "MERGED":
        merge_origin = gate.get("merge_origin") or "human_manual"
        return {
            "ok": True,
            "allowed": True,
            "gate": gate,
            "pr_state": "MERGED",
            "merge_origin": merge_origin,
            "message": f"PR already merged (origin: {merge_origin}). No merge needed.",
        }

    if pr_state == "CLOSED":
        return {
            "ok": False,
            "allowed": False,
            "gate": gate,
            "pr_state": "CLOSED",
            "error": f"PR is CLOSED without merge for {gate_id}. Merge BLOCKED.",
        }

    if gate["state"] == "approved":
        merge_origin = gate.get("merge_origin") or "harness_controlled"
        return {
            "ok": True,
            "allowed": True,
            "gate": gate,
            "pr_state": pr_state or "OPEN",
            "merge_origin": merge_origin,
            "message": (
                f"{gate_id} approved (origin: {merge_origin}). "
                "Merge allowed via harnessctl merge."
            ),
        }
    return {
        "ok": False,
        "allowed": False,
        "gate": gate,
        "error": f"{gate_id} is {gate['state']}. Merge BLOCKED.",
    }


def validate_dedicated_hitl(dedicated_root: Path) -> dict:
    manifest_path = dedicated_root / ".harness" / "manifest.json"
    if not manifest_path.exists():
        return {"valid": True, "removed_gates": [], "note": "No manifest found."}

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"valid": True, "removed_gates": [], "note": "Manifest unreadable."}

    hitl_config = manifest.get("hitl")
    if not isinstance(hitl_config, dict):
        return {"valid": True, "removed_gates": []}

    disabled = hitl_config.get("disabled_gates", [])
    if not isinstance(disabled, list):
        disabled = []

    removed_mandatory = [g for g in disabled if g in MANDATORY_GATES]

    return {
        "valid": len(removed_mandatory) == 0,
        "removed_gates": removed_mandatory,
        "all_mandatory": sorted(MANDATORY_GATES),
    }
