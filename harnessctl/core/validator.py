from __future__ import annotations

import json
from pathlib import Path


BASE_REQUIRED_FILES = [
    "README.md",
    "docs/HARNESS_BASE_CONSTITUTION.md",
    "docs/HARNESS_TAXONOMY.md",
    "docs/ARCHITECTURE_CATALOG.md",
    "docs/ARCHITECTURE_DECISION_FRAMEWORK.md",
    "docs/PATTERN_CATALOG.md",
    "docs/GO_ENGINEERING_STANDARDS.md",
    "docs/ENGINEERING_ANTI_PATTERNS.md",
    "docs/SKILL_SPECIFICATION.md",
    "docs/SKILL_CATALOG.md",
    "docs/SKILL_SPECIALIZATION.md",
    "docs/AGENT_SPECIFICATION.md",
    "docs/SQUAD_ARCHITECTURE.md",
    "docs/AGENT_AUTHORITY_MATRIX.md",
    "docs/HANDOFF_PROTOCOL.md",
    "docs/ORCHESTRATION_MODEL.md",
    "docs/WORK_ITEM_MODEL.md",
    "docs/GITHUB_PROJECT_MODEL.md",
    "docs/GITHUB_IDENTITY_GUARDRAIL.md",
    "docs/BRANCHING_POLICY.md",
    "docs/FEATURE_EXECUTION_MODEL.md",
    "docs/HITL_POLICY.md",
    "docs/WORKFLOW_STATE_MACHINE.md",
    "docs/PROJECT_LIFECYCLE.md",
    "docs/ORCHESTRATOR_GITHUB_CONTRACT.md",
    "docs/MCP_TOOLING_ARCHITECTURE.md",
    "docs/MCP_REGISTRY.md",
    "docs/MCP_PERMISSION_MODEL.md",
    "docs/TOOL_AUTHORITY_MATRIX.md",
    "docs/CUSTOM_MCP_DESIGN.md",
    "docs/HARNESS_FACTORY_ARCHITECTURE.md",
    "docs/PROJECT_PROFILE_SPECIFICATION.md",
    "docs/HARNESS_GENERATION_RULES.md",
    "docs/DEDICATED_HARNESS_SPECIFICATION.md",
    "docs/HARNESS_VERSIONING_MODEL.md",
    "docs/HARNESS_FACTORY_CONTRACT.md",
    "docs/WORKFLOW_ENGINE.md",
    "docs/WORKFLOW_CATALOG.md",
    "docs/WORKFLOW_DEFINITION_SCHEMA.md",
    "docs/WORKFLOW_FAILURE_MODEL.md",
    "docs/WORKFLOW_CONTEXT_MODEL.md",
    "docs/WORKFLOW_HANDOFF_MODEL.md",
    "docs/WORKFLOW_GUARDRAILS.md",
]


def _missing(root: Path, required: list[str]) -> list[str]:
    return [path for path in required if not (root / path).exists()]


def validate_base(root: Path) -> dict:
    missing = _missing(root, BASE_REQUIRED_FILES)
    executable = (root / "harnessctl/cli.py").exists()
    valid = not missing and executable
    return {
        "valid": valid,
        "kind": "base",
        "missing": missing,
        "checks": {
            "required_docs": not missing,
            "cli_present": executable,
        },
    }


def validate_dedicated(root: Path) -> dict:
    required = [
        ".harness/README.md",
        ".harness/project-profile.md",
        ".harness/architecture.md",
        ".harness/manifest.json",
    ]
    missing = _missing(root, required)
    manifest_valid = False
    manifest_error = None

    manifest_path = root / ".harness/manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
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
            absent = sorted(expected - set(manifest))
            if absent:
                manifest_error = f"manifest missing: {', '.join(absent)}"
            else:
                manifest_valid = True
            identity = manifest.get("confirmed_github_identity")
            if identity is not None:
                if not isinstance(identity, dict):
                    manifest_error = "confirmed_github_identity must be an object"
                    manifest_valid = False
                elif not identity.get("owner") or not identity.get("repo"):
                    manifest_error = (
                        "confirmed_github_identity requires 'owner' and 'repo'"
                    )
                    manifest_valid = False
        except json.JSONDecodeError as exc:
            manifest_error = f"invalid JSON manifest: {exc}"

    valid = not missing and manifest_valid
    return {
        "valid": valid,
        "kind": "dedicated",
        "missing": missing,
        "checks": {
            "required_files": not missing,
            "manifest_valid": manifest_valid,
        },
        "manifest_error": manifest_error,
    }
