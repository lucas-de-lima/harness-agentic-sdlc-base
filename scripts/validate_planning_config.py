from pathlib import Path
import json

FILES = [
    "docs/IMPLEMENTATION_PLANNING_AGENT.md",
    "docs/IMPLEMENTATION_WORK_BREAKDOWN.md",
    "docs/ACCEPTANCE_CRITERIA_STANDARD.md",
    "docs/IMPLEMENTATION_DEPENDENCY_MODEL.md",
    "docs/IMPLEMENTATION_SEQUENCE.md",
    "docs/PLANNING_COMPLETENESS_GATES.md",
    "docs/GITHUB_PLANNING_CONTRACT.md",
    "docs/PHASE_22_EXIT_CRITERIA.md",
    "skills/base/implementation-planning/SKILL.md",
    "workflows/implementation-planning.yaml",
    "schemas/work-item.schema.json",
]

def main():
    missing = [f for f in FILES if not Path(f).exists()]
    if missing:
        print("INVALID")
        for f in missing:
            print("- " + f)
        return 1

    schema = json.loads(Path("schemas/work-item.schema.json").read_text())
    required = set(schema["required"])
    for key in ["type", "title", "objective", "acceptance_criteria", "status"]:
        if key not in required:
            print("INVALID: schema missing", key)
            return 1

    skill = Path("skills/base/implementation-planning/SKILL.md").read_text()
    for token in ["Epic", "Feature", "User Story", "Task", "acceptance criteria", "Architecture"]:
        if token not in skill:
            print("INVALID: missing skill token", token)
            return 1

    workflow = Path("workflows/implementation-planning.yaml").read_text()
    for token in ["architecture_approved", "github_work_items", "Planning Ready", "Planning Blocked"]:
        if token not in workflow:
            print("INVALID: missing workflow token", token)
            return 1

    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
