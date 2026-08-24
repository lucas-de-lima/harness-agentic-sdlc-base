# Work Item State Machine

## Purpose

Define allowed lifecycle transitions for work items.

The Orchestrator must treat status transitions as controlled state changes, not arbitrary labels.

## States

```text
Backlog
  ↓
Ready
  ↓
In Progress
  ↓
In Review
  ├──→ Done
  └──→ In Progress
```

Any active state may move to:

```text
Blocked
```

and a resolved Blocked item returns to the state it previously occupied, normally In Progress or Ready.

## Per-level application

The state machine applies at every level of the hierarchy (see
`FEATURE_EXECUTION_MODEL.md`):

| Level | Ready → In Progress means | In Review → Done means |
|---|---|---|
| Feature | Agent claims the Feature; creates `feature/<name>` from `develop` | All Stories Done; integration review approved; `feature/<name>` merged to `develop` |
| User Story | Agent creates `story/<name>` from `feature/<name>`; starts implementing Tasks | Story Tasks implemented and validated; review approved; `story/<name>` merged to `feature/<name>` |
| Task | Agent starts the engineering action | Task implemented, validated, and reviewed (within the Story review) |

## Transition rules

### Backlog → Ready

The item has sufficient context, acceptance criteria, and dependencies are understood.

For a Feature: all Stories have acceptance criteria, dependencies are resolved or
documented as blockers, and the `feature/<name>` branch can be created from `develop`.

### Ready → In Progress

An agent has claimed the work and has the authority and required context to execute it.

### In Progress → In Review

The implementation is complete for the item's scope and required validation has been run.

For a Story: all Tasks are implemented and validated.
For a Feature: all Stories are Done and integration validation has been run.

### In Review → Done

Required reviewers and quality gates approve the work.

For a Story: review approves; `story/<name>` merged to `feature/<name>`.
For a Feature: integration review approves; `feature/<name>` merged to `develop`.

### In Review → In Progress

Review found actionable defects or missing work.

### Any active state → Blocked

A dependency, missing decision, unavailable capability, or explicit external blocker prevents progress.

### Blocked → Previous active state

The blocking condition is resolved.

## No silent transitions

An agent must not move an item to Done merely because code was produced.

Done means the item's Definition of Done has been satisfied.

## Pull requests

Where pull requests are used, the PR is evidence associated with the work item. It does not replace the issue's lifecycle state.

Story PRs target `feature/<name>`. Feature PRs target `develop`.
