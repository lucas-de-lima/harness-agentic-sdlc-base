from pathlib import Path
import sys

REQUIRED_FILES = [
    "docs/GITHUB_TO_DISCOVERY_E2E.md",
    "docs/ORCHESTRATOR_GITHUB_DISCOVERY.md",
    "docs/GITHUB_DISCOVERY_COMMENT_TEMPLATE.md",
    "docs/GITHUB_DISCOVERY_WRITE_POLICY.md",
    "docs/E2E_VALIDATION_CHECKLIST.md",
    "docs/PHASE_17_EXIT_CRITERIA.md",
    "workflows/github-discovery-e2e.yaml",
    "schemas/handoff.schema.json",
]

TOKENS = [
    "github_issue",
    "Spike",
    "Ready",
    "project-discovery",
    "execution_comment",
    "In Review",
    "Blocked",
]

def main():
    missing = [p for p in REQUIRED_FILES if not Path(p).exists()]
    if missing:
        print("INVALID")
        for p in missing:
            print(f"- missing: {p}")
        return 1
    wf = Path("workflows/github-discovery-e2e.yaml").read_text(encoding="utf-8")
    bad = [t for t in TOKENS if t not in wf]
    if bad:
        print("INVALID")
        print("Missing workflow tokens:", bad)
        return 1
    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
