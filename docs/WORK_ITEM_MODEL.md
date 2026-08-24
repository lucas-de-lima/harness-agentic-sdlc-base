# Work Item Model

## Purpose

Define the canonical representation of work for every project managed by the Agentic SDLC.

The operational backlog lives in GitHub Issues and GitHub Projects. Local repository documents are reserved for durable engineering knowledge such as architecture decisions, specifications, and project context.

## Hierarchy

The default hierarchy is:

```text
Epic
└── Feature ← unit of autonomous execution
    └── User Story ← unit of development (branch)
        └── Task ← unit of work
```

Additional types:

- Bug
- Spike
- Architecture Decision

The hierarchy is a default, not a rigid requirement. Small work may legitimately start at Feature or Task level.

## Execution roles

Each level has a distinct role in execution (see `FEATURE_EXECUTION_MODEL.md`):

| Level | Role | Branch |
|---|---|---|
| Epic | Product outcome; tracks progress via child Features | — |
| Feature | **Unit of autonomous execution** — the default boundary for assigning work to an agent | `feature/<name>` (from `develop`) |
| User Story | **Unit of development** — the branch and review boundary for a behavior | `story/<name>` (from parent `feature/<name>`) |
| Task | **Unit of work** — the finest-grained item an agent claims | — (committed on the parent `story/<name>`) |

## Definitions

### Epic

A meaningful product or system outcome that requires multiple Features.

### Feature

A coherent capability that provides user or system value and can be decomposed into User Stories. The default unit of autonomous execution: when an agent is assigned work, the boundary is the Feature.

### User Story

A behavior or outcome that can be understood and validated independently. The unit of development: each Story gets a `story/<name>` branch and is reviewed independently.

### Task

A concrete engineering action required to complete a Story. The unit of individual work.

### Bug

A defect in existing behavior.

### Spike

Time-bounded investigation performed to reduce uncertainty.

### Architecture Decision

A tracked decision concerning architecture, a significant technology choice, or a consequential trade-off. The durable decision belongs in an ADR; the GitHub item tracks the work and discussion.

## Rule

Work items describe work. Repository documentation describes durable knowledge.

Do not create local Markdown files merely to imitate GitHub cards.
