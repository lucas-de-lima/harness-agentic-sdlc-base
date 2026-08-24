from pathlib import Path
import json

FILES = [
    "docs/ARCHITECTURE_AGENT_RUNTIME.md",
    "docs/ARCHITECTURE_DECISION_OUTPUT.md",
    "docs/ARCHITECTURE_AGENT_GUARDRAILS.md",
    "docs/ARCHITECTURE_SCORECARD.md",
    "docs/ARCHITECTURE_REVIEW_CRITERIA.md",
    "docs/PHASE_18_EXIT_CRITERIA.md",
    "skills/base/architecture-deliberation/SKILL.md",
    "workflows/architecture-deliberation.yaml",
    "schemas/architecture-decision.schema.json",
    "examples/sample-project-profile.json",
]

def main():
    missing = [f for f in FILES if not Path(f).exists()]
    if missing:
        print("INVALID")
        for f in missing:
            print("- " + f)
        return 1

    schema = json.loads(Path("schemas/architecture-decision.schema.json").read_text())
    required = set(schema["required"])
    expected = {
        "selected_architecture",
        "confidence",
        "context",
        "candidates",
        "simplicity_baseline",
        "rationale",
        "rejected_alternatives",
        "consequences",
        "future_pressure",
        "unresolved_questions",
    }
    if required != expected:
        print("INVALID: architecture decision schema mismatch")
        return 1

    skill = Path("skills/base/architecture-deliberation/SKILL.md").read_text()
    for token in ["simplest viable", "rejected alternatives", "Do not implement code"]:
        if token not in skill:
            print(f"INVALID: missing skill rule: {token}")
            return 1

    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
