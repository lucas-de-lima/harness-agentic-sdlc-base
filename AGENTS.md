# Agentic SDLC Base

## Repository role

This is the Base Harness repository. It defines reusable governance, skills,
workflows, tooling, templates, and the Harness Factory used to create
Dedicated Harnesses for unrelated product repositories.

## Before changing anything

1. Read `docs/HARNESS_BASE_CONSTITUTION.md`.
2. Read `docs/HARNESS_TAXONOMY.md`.
3. Identify the governing phase/contract for the change.
4. Keep Base capabilities generic.
5. Prefer deterministic tooling over agentic behavior when the task is deterministic.
6. Run `make validate` and `make test` when applicable.

## Base vs project boundary

Do not place product-specific domain assumptions in this repository.

A capability belongs in the Base Harness only when it is reusable across
unrelated product repositories.

Project-specific behavior belongs in the Dedicated Harness.

## Runtime projections

Canonical skills live under `skills/base/`.

Codex runtime projections may live under `.codex/skills/`.

Do not make Codex-specific syntax the source of truth for governance.

## Safety

- Do not add unrestricted agent authority.
- Do not add broad MCP access without an approved capability need.
- Do not create autonomous loops without bounded termination.
- Do not silently weaken Base Constitution rules.
