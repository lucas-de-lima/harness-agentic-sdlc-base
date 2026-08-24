from __future__ import annotations

import json
import sys
from pathlib import Path

REQUIRED = [
    ".harness/README.md",
    ".harness/manifest.json",
    ".harness/project-profile.md",
    ".harness/architecture.md",
]


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_dedicated_harness.py <project-root>")
        return 2

    root = Path(sys.argv[1]).resolve()
    missing = [p for p in REQUIRED if not (root / p).exists()]
    if missing:
        print("INVALID")
        for p in missing:
            print("- missing:", p)
        return 1

    try:
        manifest = json.loads((root / ".harness/manifest.json").read_text(encoding="utf-8"))
    except Exception as exc:
        print("INVALID manifest:", exc)
        return 1

    expected = {
        "schema_version",
        "harness_version",
        "base_harness_version",
        "project_repository",
        "architecture_profile",
        "selected_agents",
        "selected_skills",
        "selected_tools",
        "enabled_workflows",
    }
    absent = expected - set(manifest)
    if absent:
        print("INVALID manifest missing:", sorted(absent))
        return 1

    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
