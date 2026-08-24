from pathlib import Path
import json

FILES = [
    "docs/REVIEW_AGENT_RUNTIME.md",
    "docs/REVIEW_CRITERIA_MODEL.md",
    "docs/ARCHITECTURE_REVIEW_WORKFLOW.md",
    "docs/REVIEW_REPORT_SCHEMA.md",
    "docs/REVIEW_HANDOFF_MODEL.md",
    "docs/REVIEW_GUARDRAILS.md",
    "docs/PHASE_20_EXIT_CRITERIA.md",
    "skills/base/architecture-review/SKILL.md",
    "workflows/architecture-review.yaml",
    "schemas/review-report.schema.json",
]

def main():
    missing=[f for f in FILES if not Path(f).exists()]
    if missing:
        print("INVALID")
        for f in missing: print("- "+f)
        return 1
    schema=json.loads(Path("schemas/review-report.schema.json").read_text())
    required=set(schema["required"])
    for token in ["decision","findings","gates"]:
        if token not in required:
            print("INVALID: schema missing", token)
            return 1
    skill=Path("skills/base/architecture-review/SKILL.md").read_text()
    for token in ["Approved","Changes Requested","Blocked","Do not implement fixes"]:
        if token not in skill:
            print("INVALID: missing skill token", token)
            return 1
    wf=Path("workflows/architecture-review.yaml").read_text()
    for token in ["source_workflow: WF-002","Architecture Ready","In Progress","Blocked"]:
        if token not in wf:
            print("INVALID: missing workflow token", token)
            return 1
    print("VALID")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
