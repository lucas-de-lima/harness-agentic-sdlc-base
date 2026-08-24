from pathlib import Path
import sys

REQUIRED = [
    "docs/GITHUB_PROJECT_BOOTSTRAP_RUNBOOK.md",
    "docs/GITHUB_PROJECT_FIELDS.md",
    "docs/GITHUB_PROJECT_VIEWS.md",
    "docs/DISCOVERY_001_SPEC.md",
    "docs/PROJECT_AUTOMATION_POLICY.md",
    "docs/GITHUB_PROJECT_TEMPLATE_STRATEGY.md",
    "docs/PHASE_16_EXIT_CRITERIA.md",
    "github/DISCOVERY-001.md",
]

def main() -> int:
    missing = [p for p in REQUIRED if not (Path(".") / p).exists()]
    if missing:
        print("INVALID")
        for p in missing:
            print(p)
        return 1
    issue = Path("github/DISCOVERY-001.md").read_text(encoding="utf-8")
    required = ["Type", "Spike", "Status", "Ready", "Phase", "Discovery", "Acceptance criteria"]
    missing_text = [x for x in required if x not in issue]
    if missing_text:
        print("INVALID")
        print("Discovery spec missing:", missing_text)
        return 1
    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
