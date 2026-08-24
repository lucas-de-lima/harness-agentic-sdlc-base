from pathlib import Path
import json

FILES = [
    "docs/GO_ENGINEER_E2E.md",
    "docs/GO_ENGINEER_E2E_WORKFLOW.md",
    "docs/GO_ENGINEER_E2E_TASK_SELECTION.md",
    "docs/IMPLEMENTATION_E2E_VALIDATION.md",
    "docs/IMPLEMENTATION_E2E_COMMENT.md",
    "docs/IMPLEMENTATION_ROLLBACK_POLICY.md",
    "docs/PHASE_25_EXIT_CRITERIA.md",
    "workflows/go-engineer-e2e.yaml",
    "schemas/implementation-e2e-result.schema.json",
]

def main():
    missing = [f for f in FILES if not Path(f).exists()]
    if missing:
        print("INVALID")
        for f in missing:
            print("- " + f)
        return 1

    schema = json.loads(Path("schemas/implementation-e2e-result.schema.json").read_text())
    for key in ["execution_id", "work_item_id", "status", "modified_files", "tests", "validation", "handoff"]:
        if key not in schema["required"]:
            print("INVALID: missing result field", key)
            return 1

    wf = Path("workflows/go-engineer-e2e.yaml").read_text()
    for token in [
        "required_type: Task",
        "required_status: Ready",
        "to: In Progress",
        "to: In Review",
        "architecture_change",
        "task_done",
    ]:
        if token not in wf:
            print("INVALID: missing workflow rule", token)
            return 1

    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
