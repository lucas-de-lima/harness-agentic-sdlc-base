# Base Harness Layout

## Canonical structure

```text
agentic-sdlc-base/
├── .codex/
│   └── skills/
├── agents/
│   └── base/
├── config/
├── docs/
├── examples/
├── schemas/
├── scripts/
├── skills/
│   └── base/
├── templates/
├── workflows/
├── AGENTS.md
├── Dockerfile
├── Makefile
└── README.md
```

## Ownership

### `docs/`

Durable governance, architecture, runtime, SDLC, and release contracts.

### `skills/`

Canonical reusable agent skills.

### `agents/`

Agent role definitions and configuration.

### `workflows/`

Executable workflow declarations.

### `schemas/`

Machine-checkable artifact contracts.

### `templates/`

Templates generated or consumed by the Harness Factory.

### `scripts/`

Deterministic validation and automation.

### `.codex/`

Runtime adapter layer for Codex-specific skill loading.

## Rule

This repository is the Base Harness, not a product. Product code must not be placed here merely for convenience.
