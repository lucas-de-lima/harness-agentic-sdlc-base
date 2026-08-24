from pathlib import Path
import json

FILES = [
    "docs/ARCHITECTURE_REVIEW_E2E.md",
    "docs/ARCHITECTURE_REVIEW_E2E_WORKFLOW.md",
    "docs/ARCHITECTURE_REVIEW_COMMENT.md",
    "docs/IMPLEMENTATION_PLANNING_GATE.md",
    "docs/REVIEW_LOOP_MODEL.md",
    "docs/PHASE_21_EXIT_CRITERIA.md",
    "workflows/architecture-review-e2e.yaml",
    "schemas/review-e2e.schema.json",
]

def main():
    missing = [f for f in FILES if not Path(f).exists()]
    if missing:
        print("INVALID")
        for f in missing:
            print("- " + f)
        return 1

    schema = json.loads(Path("schemas/review-e2e.schema.json").read_text())
    if "Approved" not in schema["properties"]["decision"]["enum"]:
        print("INVALID")
        return 1

    wf = Path("workflows/architecture-review-e2e.yaml").read_text()
    for token in ["Architecture Ready", "Architecture Approved", "implementation-planning", "In Progress", "Blocked"]:
        if token not in wf:
            print("INVALID:", token)
            return 1

    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
