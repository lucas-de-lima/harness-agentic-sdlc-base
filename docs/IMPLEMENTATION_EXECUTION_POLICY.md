# Implementation Execution Policy

## Execution unit

The default unit of autonomous execution is the **Feature** (see
`FEATURE_EXECUTION_MODEL.md`). An agent may also claim a single Task for small, isolated
work, but the Feature is the standard boundary.

## Claiming a Feature

A Go Engineer may claim a Feature whose status is `Ready` and whose `feature/<name>` branch
can be created from `develop`.

Before changing code:

1. read the Feature and its User Stories
2. inspect acceptance criteria for each Story
3. inspect dependencies (Feature-level and Task-level)
4. inspect architecture
5. inspect current repository state
6. confirm the Feature is in scope and blockers are cleared

Then transition:

`Feature Ready → In Progress`

Create the `feature/<name>` branch from `develop`.

## Claiming a Task (small work)

For small, isolated work (single Story, single Task), an agent may claim a Task whose
status is `Ready`. The same pre-work steps apply, scoped to the Task.

## Story development

Within a Feature, the agent works through User Stories:

1. Create `story/<name>` branch from `feature/<name>`.
2. Implement the Story's Tasks on the `story/<name>` branch.
3. Stay inside the files and behavior materially related to the Story.
4. Validate (gofmt, go test, go vet, etc.).
5. Transition: `Story In Progress → In Review`.
6. Request independent review (WF-006).
7. On approval: merge `story/<name>` → `feature/<name>`. Story → Done.

Unexpected required changes must trigger deliberation rather than silent scope expansion.

## Scope

The agent should stay inside the files and behavior materially related to the Feature and
its Stories. Cross-Feature changes require explicit escalation.

## Validation

At minimum, run relevant:

- `gofmt`
- `go test`
- `go vet`

Project-specific checks may add:

- race detector
- integration tests
- lint
- benchmarks
- container tests

Validation runs per Story (before Story In Review) and per Feature (before Feature In
Review — integration validation).

## Git hygiene

The agent should inspect:

- `git status`
- `git diff`
- changed files

before each Story handoff and before the Feature handoff.

Use `harnessctl branch-check` to validate branch lineage before starting work.

## Completion

When all Stories in the Feature are Done:

`Feature In Progress → In Review`

The Engineer must not set Feature `Done`. That belongs to the review/approval step.

For Task-level execution: `Task In Progress → In Review`. The Engineer must not set
Task `Done`.
