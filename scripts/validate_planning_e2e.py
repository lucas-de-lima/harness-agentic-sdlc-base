from pathlib import Path
import json

FILES = [
    "docs/IMPLEMENTATION_PLANNING_E2E.md",
    "docs/IMPLEMENTATION_PLANNING_E2E_WORKFLOW.md",
    "docs/GITHUB_WORK_BREAKDOWN_RULES.md",
    "docs/PLANNING_EVIDENCE_COMMENT.md",
    "docs/PLANNING_TO_IMPLEMENTATION_GATE.md",
    "docs/PHASE_23_EXIT_CRITERIA.md",
    "workflows/implementation-planning-e2e.yaml",
    "schemas/planning-result.schema.json",
]

def main():
    missing=[f for f in FILES if not Path(f).exists()]
    if missing:
        print("INVALID")
        for f in missing:
            print("- "+f)
        return 1

    schema=json.loads(Path("schemas/planning-result.schema.json").read_text())
    for key in ["epic","features","user_stories","tasks","first_ready_task"]:
        if key not in schema["required"]:
            print("INVALID:", key)
            return 1

    wf=Path("workflows/implementation-planning-e2e.yaml").read_text()
    for token in ["Architecture Approved","create_epic","create_task","Backlog_to_Ready: true","Ready_to_In_Progress: false","Planning Ready"]:
        if token not in wf:
            print("INVALID:", token)
            return 1

    print("VALID")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
