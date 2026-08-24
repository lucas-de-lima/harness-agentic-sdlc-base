from pathlib import Path

FILES = [
    "docs/harness-factory/DEDICATED_HARNESS_BOOTSTRAP.md",
    "docs/harness-factory/PROJECT_INPUT_DISCOVERY.md",
    "docs/harness-factory/CAPABILITY_SELECTION.md",
    "docs/harness-factory/GENERATION_MODES.md",
    "docs/harness-factory/BOOTSTRAP_VALIDATION.md",
    "docs/harness-factory/BOOTSTRAP_DIFF_POLICY.md",
    "docs/harness-factory/BOOTSTRAP_COMMANDS.md",
    "docs/PHASE_30_EXIT_CRITERIA.md",
    "templates/dedicated-harness/.harness/manifest.yaml",
    "scripts/bootstrap_dedicated_harness.py",
    "scripts/validate_dedicated_harness.py",
    "scripts/audit_bootstrap_diff.py",
    "schemas/dedicated-harness-manifest.schema.json",
]

def main():
    missing = [p for p in FILES if not Path(p).exists()]
    if missing:
        print("INVALID")
        for p in missing:
            print("-", p)
        return 1
    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
