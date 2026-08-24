from pathlib import Path
import json

FILES = [
    "docs/SDLC_COMPLETION_MODEL.md",
    "docs/RELEASE_GATE_MODEL.md",
    "docs/RELEASE_CANDIDATE_WORKFLOW.md",
    "docs/RELEASE_REPORT_SCHEMA.md",
    "docs/DOCKER_RELEASE_MODEL.md",
    "docs/SECURITY_RELEASE_MODEL.md",
    "docs/DOCUMENTATION_RELEASE_MODEL.md",
    "docs/PHASE_28_EXIT_CRITERIA.md",
    "workflows/release-candidate.yaml",
    "schemas/release-report.schema.json",
]

def main():
    missing = [f for f in FILES if not Path(f).exists()]
    if missing:
        print("INVALID")
        for f in missing:
            print("- " + f)
        return 1

    schema = json.loads(Path("schemas/release-report.schema.json").read_text())
    for key in ["final_decision", "residual_risks", "waivers"]:
        if key not in schema["required"]:
            print("INVALID: missing report field", key)
            return 1

    wf = Path("workflows/release-candidate.yaml").read_text()
    for token in ["required_state: Release Candidate", "Release Ready", "Release Blocked"]:
        if token not in wf:
            print("INVALID: missing workflow rule", token)
            return 1

    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
