from pathlib import Path
import sys

REQUIRED = [
    "docs/GITHUB_INTEGRATION_CONTRACT.md",
    "docs/GITHUB_PROJECT_BOOTSTRAP.md",
    "docs/GITHUB_MCP_PHASE14.md",
    "docs/GITHUB_STATE_MAPPING.md",
    "docs/GITHUB_EXECUTION_EVIDENCE.md",
    "workflows/github-discovery.yaml",
]

def main() -> int:
    root = Path(".")
    missing = [p for p in REQUIRED if not (root / p).exists()]
    if missing:
        print("INVALID")
        for p in missing:
            print(f"- {p}")
        return 1

    text = (root / "workflows/github-discovery.yaml").read_text(encoding="utf-8")
    required_tokens = [
        "github_issue",
        "project_fields",
        "execution_comment",
        "In Review",
        "Blocked",
    ]
    bad = [token for token in required_tokens if token not in text]
    if bad:
        print("INVALID")
        print("Missing tokens:", bad)
        return 1

    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
