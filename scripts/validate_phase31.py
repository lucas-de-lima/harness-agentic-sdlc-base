from pathlib import Path
FILES = [
    "docs/real-project/REAL_PROJECT_DISCOVERY.md",
    "docs/real-project/REAL_PROJECT_DISCOVERY_FLOW.md",
    "docs/real-project/PROJECT_PROFILE_REAL_TEMPLATE.md",
    "docs/real-project/EVIDENCE_INDEX.md",
    "docs/real-project/REAL_PROJECT_HANDOFF.md",
    "docs/PHASE_31_EXIT_CRITERIA.md",
    "schemas/project-profile-real.schema.json",
    "scripts/inspect_real_project.py",
    "scripts/create_project_profile_skeleton.py",
]
def main():
    missing=[p for p in FILES if not Path(p).exists()]
    if missing:
        print("INVALID")
        for p in missing: print("- "+p)
        return 1
    print("VALID")
    return 0
if __name__=="__main__":
    raise SystemExit(main())
