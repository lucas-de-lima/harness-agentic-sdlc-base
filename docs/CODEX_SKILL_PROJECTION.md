# Codex Skill Projection

## Purpose

Define how abstract Base Harness skills become executable Codex skills.

## Model

```text
Base Skill Specification
        ↓
Codex Skill Adapter
        ↓
SKILL.md
        ↓
optional references/scripts/assets
```

## Projection rules

The adapter must preserve:

- purpose
- trigger conditions
- required inputs
- outputs
- prohibited behavior
- validation expectations

It may adapt:

- wording
- command syntax
- references
- tool hints

It must not change the governing intent of the Base Skill.

## Dedicated Harness

A Dedicated Harness may add a project-specific skill under its runtime skills directory.

Project skills should complement rather than duplicate Base skills.

## Bundled resources

Use bundled resources only when they reduce repeated context or provide deterministic procedures.

Codex's current skill model supports optional `agents/`, scripts, references, and assets in a skill package. citeturn817121search2
