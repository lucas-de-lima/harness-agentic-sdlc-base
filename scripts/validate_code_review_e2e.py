from pathlib import Path
import json

FILES = [
    "docs/CODE_REVIEW_E2E_WORKFLOW.md",
    "docs/CODE_REVIEW_E2E_EXECUTION.md",
    "docs/CODE_REVIEW_APPROVAL_GATE.md",
    "docs/CODE_REVIEW_CHANGES_REQUESTED_LOOP.md",
    "docs/CODE_REVIEW_BLOCKED_LOOP.md",
    "docs/CODE_REVIEW_E2E_VALIDATION.md",
    "docs/PHASE_27_EXIT_CRITERIA.md",
    "workflows/code-review-e2e.yaml",
    "schemas/code-review-e2e-result.schema.json",
]

def main():
    missing=[f for f in FILES if not Path(f).exists()]
    if missing:
        print("INVALID")
        for f in missing: print("- "+f)
        return 1

    schema=json.loads(Path("schemas/code-review-e2e-result.schema.json").read_text())
    if "decision" not in schema["required"] or "final_state" not in schema["required"]:
        print("INVALID: schema incomplete")
        return 1

    wf=Path("workflows/code-review-e2e.yaml").read_text()
    for token in [
        "required_status: In Review",
        "state: Done",
        "state: In Progress",
        "state: Blocked",
        "source_code",
        "review_handoff",
    ]:
        if token not in wf:
            print("INVALID:", token)
            return 1

    print("VALID")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
