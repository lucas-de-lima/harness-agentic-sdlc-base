from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .vault import materialize_vault


REQUIRED_PROFILE_KEYS = {
    "schema_version",
    "identity",
    "domain",
    "technical",
    "constraints",
    "risks",
    "open_questions",
}


def _slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "project"


def _markdown_list(items: list[str]) -> str:
    if not items:
        return "- None identified."
    return "\n".join(f"- {item}" for item in items)


def _format_oq(oq: str | dict) -> str:
    if isinstance(oq, str):
        return f"- {oq} (type: engineering, impact: medium)"
    q_type = oq.get("type", "engineering")
    impact = oq.get("impact", "medium")
    question = oq.get("question", "")
    resolved = oq.get("resolved", False)
    label = f"- {question} [type: {q_type}, impact: {impact}]"
    if resolved:
        label += " [RESOLVED]"
    return label


def _load_profile(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Project Profile must be a JSON object.")
    missing = sorted(REQUIRED_PROFILE_KEYS - set(data))
    if missing:
        raise ValueError(f"Project Profile missing keys: {', '.join(missing)}")
    return data


def generate_harness(
    profile_path: Path,
    base_version: str,
    output_path: Path,
) -> dict[str, Any]:
    profile = _load_profile(profile_path)
    identity = profile["identity"]
    domain = profile["domain"]
    technical = profile["technical"]
    constraints = profile["constraints"]
    risks = profile["risks"]
    open_questions = profile["open_questions"]

    name = str(identity["proposed_product_name"])
    repo = str(identity["proposed_repository_name"])
    architecture = str(identity.get("selected_architecture", "pending-deliberation"))
    harness_version = "0.1.0"

    out = output_path
    out.mkdir(parents=True, exist_ok=True)

    (out / ".harness").mkdir(exist_ok=True)
    for sub in [
        "agents",
        "skills",
        "policies",
        "workflows",
        "tools",
        "context",
    ]:
        (out / ".harness" / sub).mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": "1",
        "harness_version": harness_version,
        "base_harness_version": base_version,
        "project_repository": repo,
        "architecture_profile": architecture,
        "selected_agents": [],
        "selected_skills": [],
        "selected_tools": [],
        "enabled_workflows": [],
        "confirmed_github_identity": None,
    }
    (out / ".harness" / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )

    (out / ".harness" / "README.md").write_text(
        f"""# {name} Dedicated Harness

Generated from Harness Base `{base_version}`.

This harness is project-owned after commit. Base Harness changes do not
automatically overwrite it.

## Project

- Product: {name}
- Repository: {repo}
- Architecture: {architecture}

## Structure

- `project-profile.md` — discovery model
- `architecture.md` — selected architecture and rationale
- `context/` — durable project context
- `agents/` — project-specific agent configuration
- `skills/` — project skill overlays
- `policies/` — project constraints
- `workflows/` — enabled workflows
- `tools/` — project tool configuration
""",
        encoding="utf-8",
    )

    (out / ".harness" / "project-profile.md").write_text(
        f"""# Project Profile

## Identity

- Product: {name}
- Repository: {repo}

## Problem

{identity.get("problem_statement", "Not yet captured.")}

## Description

{identity.get("short_description", "Not yet captured.")}

## Domain

### Actors

{_markdown_list(domain.get("actors", []))}

### Core concepts

{_markdown_list(domain.get("core_concepts", []))}

### Entities

{_markdown_list(domain.get("entities", []))}

### Business rules

{_markdown_list(domain.get("business_rules", []))}

## Technical

- Application type: {technical.get("application_type", "Unknown")}
- Persistence: {technical.get("persistence", "Unknown")}
- Interfaces: {", ".join(technical.get("interfaces", [])) or "None identified"}
- External dependencies: {", ".join(technical.get("external_dependencies", [])) or "None identified"}

## Constraints

{_markdown_list(constraints if isinstance(constraints, list) else [])}

## Risks

{_markdown_list(risks if isinstance(risks, list) else [])}

## Open questions

{_markdown_list([_format_oq(oq) for oq in open_questions]) if open_questions else "- None identified."}
""",
        encoding="utf-8",
    )

    (out / ".harness" / "architecture.md").write_text(
        f"""# Architecture

## Current decision

`{architecture}`

## Status

This file is generated from the current project profile. A final architecture
decision must be backed by the Architecture Decision workflow and ADRs before
implementation proceeds.

## Principle

Use the simplest architecture that satisfies the project requirements.
""",
        encoding="utf-8",
    )

    result = {
        "valid": True,
        "project": name,
        "repository": repo,
        "base_harness_version": base_version,
        "dedicated_harness_version": harness_version,
        "output": str(out),
        "warnings": [],
    }
    if open_questions:
        result["warnings"].append(
            f"{len(open_questions)} open question(s) remain; architecture or implementation may need escalation."
        )

    # Materialize vault into dedicated harness
    vault_result = materialize_vault(
        base_root=Path(__file__).resolve().parents[2],
        dedicated_root=out,
        selected_ids=None,
        base_version=base_version,
    )
    if vault_result.get("ok"):
        result["vault"] = {
            "materialized": True,
            "notes": vault_result["note_ids"],
        }
    else:
        result["warnings"].append("Vault not materialized: " + vault_result.get("error", "unknown"))

    return result
