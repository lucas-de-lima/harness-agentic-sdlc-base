from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED = [
    "AGENTS.md",
    "README.md",
    "harness-manifest.yaml",
    "docs/HARNESS_BASE_CONSTITUTION.md",
    "docs/HARNESS_TAXONOMY.md",
    "docs/ARCHITECTURE_CATALOG.md",
    "docs/GO_ENGINEERING_STANDARDS.md",
    "docs/SKILL_SPECIFICATION.md",
    "docs/AGENT_SPECIFICATION.md",
    "docs/WORKFLOW_ENGINE.md",
    "docs/MCP_TOOLING_ARCHITECTURE.md",
    "docs/HARNESS_FACTORY_ARCHITECTURE.md",
    "docs/SDLC_COMPLETION_MODEL.md",
    "docs/RELEASE_GATE_MODEL.md",
    "docs/governance/BASE_HARNESS_LAYOUT.md",
    "docs/governance/CAPABILITY_OWNERSHIP.md",
    "docs/governance/BASE_HARNESS_DOD.md",
    "docs/governance/VERSIONING_AND_RELEASE.md",
]

SKILLS = [
    "skills/base/project-discovery/SKILL.md",
    "skills/base/architecture-deliberation/SKILL.md",
    "skills/base/architecture-review/SKILL.md",
    "skills/base/implementation-planning/SKILL.md",
    "skills/base/go-engineer/SKILL.md",
    "skills/base/code-review/SKILL.md",
]

WORKFLOWS = [
    "workflows/github-discovery-e2e.yaml",
    "workflows/architecture-e2e.yaml",
    "workflows/architecture-review-e2e.yaml",
    "workflows/implementation-planning-e2e.yaml",
    "workflows/go-engineer-e2e.yaml",
    "workflows/code-review-e2e.yaml",
    "workflows/release-candidate.yaml",
]

VAULT = [
    "vault/_index.md",
    "vault/governance.md",
    "vault/architecture.md",
    "vault/agents.md",
    "vault/skills.md",
    "vault/workflows.md",
    "vault/policies.md",
    "vault/tools.md",
]

def main() -> int:
    missing = [p for p in REQUIRED + SKILLS + WORKFLOWS + VAULT if not (ROOT / p).exists()]
    if missing:
        print("INVALID")
        for p in missing:
            print("- missing:", p)
        return 1

    # Validate JSON schemas that are part of the cumulative harness.
    for schema in ROOT.glob("schemas/*.json"):
        try:
            data = json.loads(schema.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError("schema root is not an object")
        except Exception as exc:
            print(f"INVALID schema {schema}: {exc}")
            return 1

    print("VALID")
    print(f"Required files: {len(REQUIRED)}")
    print(f"Canonical skills: {len(SKILLS)}")
    print(f"Canonical workflows: {len(WORKFLOWS)}")
    print(f"Vault notes: {len(VAULT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
