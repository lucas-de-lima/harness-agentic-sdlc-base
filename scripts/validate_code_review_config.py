from pathlib import Path
import json

FILES = [
    "docs/CODE_REVIEW_AGENT.md",
    "docs/CODE_REVIEW_CRITERIA.md",
    "docs/CODE_REVIEW_WORKFLOW.md",
    "docs/CODE_REVIEW_HANDOFF.md",
    "docs/CODE_REVIEW_EVIDENCE.md",
    "docs/CODE_REVIEW_GUARDRAILS.md",
    "docs/CODE_REVIEW_E2E.md",
    "docs/CODE_REVIEW_E2E_VALIDATION.md",
    "docs/PHASE_26_EXIT_CRITERIA.md",
    "docs/PHASE_26B_EXIT_CRITERIA.md",
    "skills/base/code-review/SKILL.md",
    "workflows/code-review.yaml",
    "schemas/code-review-result.schema.json",
]

def main():
    missing = [f for f in FILES if not Path(f).exists()]
    if missing:
        print("INVALID")
        for f in missing:
            print("- " + f)
        return 1

    schema = json.loads(Path("schemas/code-review-result.schema.json").read_text())
    for key in ["decision", "findings", "gates"]:
        if key not in schema["required"]:
            print("INVALID: missing", key)
            return 1

    skill = Path("skills/base/code-review/SKILL.md").read_text()
    for token in ["actual Git diff", "Approved", "Changes Requested", "Blocked", "Do not modify"]:
        if token not in skill:
            print("INVALID: missing skill rule", token)
            return 1

    wf = Path("workflows/code-review.yaml").read_text()
    for token in ["required_status: In Review", "to: Done", "to: In Progress", "to: Blocked", "source_code"]:
        if token not in wf:
            print("INVALID: missing workflow rule", token)
            return 1

    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
