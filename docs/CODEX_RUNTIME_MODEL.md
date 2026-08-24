# Codex Runtime Model

## Purpose

Define how the Agentic SDLC Base maps its abstract capabilities onto the current Codex runtime.

## Runtime layers

```text
Base Harness
    ↓
Codex runtime projection
    ↓
AGENTS.md + SKILL.md
    ↓
Current task / repository
```

## AGENTS.md

Codex discovers `AGENTS.md` files from the project root toward the current working directory. More deeply scoped files can take precedence when instructions conflict. The active runtime also supports `AGENTS.override.md` as a local override mechanism. citeturn817121search1turn817121search10

Our policy:

- Base repository rules live in root `AGENTS.md`.
- Product-specific runtime instructions may live in the product repository.
- The Dedicated Harness must not rely on hidden, undeclared prompt state.
- Runtime-specific instructions are a projection of the Harness model, not the Harness model itself.

## Skills

Codex skills use a directory containing a required `SKILL.md`. The file uses YAML frontmatter with `name` and `description`; bundled scripts, references, and assets are optional. citeturn817121search2

The Base Harness therefore treats a skill as a portable capability package.

## Source of truth

The Base Harness skill specification remains authoritative for lifecycle/governance.

The Codex `SKILL.md` is the runtime adapter.

Do not put governance that is required by another runtime only in Codex-specific syntax.

## Current implementation stance

For this phase, we use repository-local skills. Remote API skill distribution is intentionally deferred.
