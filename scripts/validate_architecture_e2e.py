from pathlib import Path
import json
import sys

FILES = [
    "docs/ARCHITECTURE_E2E.md",
    "docs/ARCHITECTURE_E2E_WORKFLOW.md",
    "docs/ARCHITECTURE_REVIEW_HANDOFF.md",
    "docs/ADR_TEMPLATE.md",
    "docs/ARCHITECTURE_DECISION_VALIDATION.md",
    "docs/PHASE_19_EXIT_CRITERIA.md",
    "workflows/architecture-e2e.yaml",
    "schemas/architecture-handoff.schema.json",
    "skills/base/architecture-deliberation/SKILL.md",
]

def main() -> int:
    missing = [f for f in FILES if not Path(f).exists()]
    if missing:
        print("INVALID")
        for f in missing:
            print("- " + f)
        return 1

    schema = json.loads(Path("schemas/architecture-handoff.schema.json").read_text())
    required = set(schema["required"])
    if "selected_architecture" not in required or "simplicity_baseline" not in required:
        print("INVALID: incomplete handoff schema")
        return 1

    skill = Path("skills/base/architecture-deliberation/SKILL.md").read_text()
    for token in ["simplest viable", "rejected alternatives", "Do not implement code"]:
        if token not in skill:
            print("INVALID: missing skill rule:", token)
            return 1

    workflow = Path("workflows/architecture-e2e.yaml").read_text()
    for token in ["architecture-deliberation", "Architecture Ready", "Architecture Blocked", "production_code"]:
        if token not in workflow:
            print("INVALID: missing workflow token:", token)
            return 1

    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
