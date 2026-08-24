from pathlib import Path
import json

FILES = [
    "docs/GO_ENGINEER_AGENT.md",
    "docs/IMPLEMENTATION_EXECUTION_POLICY.md",
    "docs/GO_ENGINEER_CHANGE_BOUNDARY.md",
    "docs/IMPLEMENTATION_VALIDATION_GATES.md",
    "docs/IMPLEMENTATION_HANDOFF.md",
    "docs/IMPLEMENTATION_FAILURE_MODEL.md",
    "docs/IMPLEMENTATION_REVIEW_CONTRACT.md",
    "docs/PHASE_24_EXIT_CRITERIA.md",
    "skills/base/go-engineer/SKILL.md",
    "workflows/implementation.yaml",
    "schemas/implementation-handoff.schema.json",
]

def main():
    missing = [f for f in FILES if not Path(f).exists()]
    if missing:
        print("INVALID")
        for f in missing:
            print("- " + f)
        return 1

    schema = json.loads(Path("schemas/implementation-handoff.schema.json").read_text())
    for key in [
        "work_item_id",
        "workflow_id",
        "execution_id",
        "tests_run",
        "validation_results",
        "acceptance_criteria_results",
    ]:
        if key not in schema["required"]:
            print("INVALID: missing handoff field", key)
            return 1

    skill = Path("skills/base/go-engineer/SKILL.md").read_text()
    for token in [
        "smallest correct",
        "gofmt",
        "go test ./...",
        "go vet ./...",
        "architectural change",
        "Do not mark the Task Done",
    ]:
        if token not in skill:
            print("INVALID: missing skill rule", token)
            return 1

    wf = Path("workflows/implementation.yaml").read_text()
    for token in [
        "required_status: Ready",
        "claim: In Progress",
        "success: In Review",
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
