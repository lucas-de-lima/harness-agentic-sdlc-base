# Feature Execution Model

## Purpose

Define Feature as the default unit of autonomous SDLC execution. This model specifies how
the four-level work-item hierarchy maps to execution, branching, and review boundaries.

## Hierarchy with execution roles

```text
Epic
└── Feature ← unit of autonomous execution (external boundary)
    └── User Story ← unit of development (branch boundary)
        └── Task ← unit of work (individual engineering action)
```

## Unit definitions

### Epic — product outcome

- A meaningful product or system outcome that requires multiple Features.
- Never the direct target of autonomous execution.
- Tracks progress via its child Features.

### Feature — execution unit

- A coherent capability that provides user or system value.
- **The default unit of autonomous execution.** When an agent is assigned work, the
  boundary is the Feature, not an individual Task.
- Owns a `feature/<name>` branch created from `develop`.
- An execution cycle targets one Feature: the agent works through the Feature's Stories
  and Tasks, creating `story/<name>` branches as needed, until the Feature is complete and
  reviewed.
- A Feature is `Ready` for execution when:
  - Its User Stories have acceptance criteria.
  - Its Tasks have material dependencies resolved (or the unresolved ones are documented
    as blockers).
  - The parent Feature's blockers (OQs, architecture, upstream Features) are cleared or
    explicitly scoped as non-blocking.
  - The `feature/<name>` branch can be created from `develop`.
- A Feature is `Done` when all its User Stories are `Done` and the `feature/<name>` branch
  has been merged to `develop` after review.

### User Story — development unit

- A behavior or outcome that can be understood and validated independently.
- **The unit of development and branching.** Each User Story gets a `story/<name>` branch
  created from the parent `feature/<name>` branch.
- An agent implements the Story's Tasks on the `story/<name>` branch.
- A Story is `In Review` when its Tasks are implemented and validated.
- A Story is `Done` when its review is approved and the `story/<name>` branch is merged
  back to the parent `feature/<name>` branch.

### Task — work unit

- A concrete engineering action required to complete a Story.
- **The unit of individual work.** A Task is the finest-grained item an agent claims.
- A Task is `Ready` when its dependencies are resolved.
- A Task transitions: `Ready → In Progress → In Review → Done`.
- Multiple Tasks within a Story may be implemented sequentially or in parallel (on separate
  `story/` branches) when file ownership and dependencies allow.

## Execution flow

```text
Feature Ready
    ↓
Agent claims Feature (WF-005 trigger)
    ↓
Create feature/<name> branch from develop
    ↓
For each User Story in the Feature:
    ├── Create story/<name> branch from feature/<name>
    ├── Implement Tasks on story/<name>
    ├── Validate (gofmt, go test, go vet, etc.)
    ├── Story In Review
    ├── Review approves
    ├── ⏸ Human Gate: HG-MERGE-STORY (merge story/<name> → feature/<name>)
    ├── [human approves] → merge, Story Done
    └── [human rejects] → Story In Progress (remediate)
    ↓
All Stories Done
    ↓
Feature In Review (integration review on feature/<name>)
    ↓
Review approves
    ↓
⏸ Human Gate: HG-MERGE-FEATURE (merge feature/<name> → develop)
    ↓ [human approves]
Feature Done
    ↓
Release Candidate ready
    ↓
⏸ Human Gate: HG-RELEASE (release / tag / publish)
⏸ Human Gate: HG-MERGE-DEVELOP (merge develop → main) [if not already on main]
    ↓ [human approves]
Released
```

The ⏸ symbol marks a Human Gate (see `HITL_POLICY.md`). The workflow PAUSES at each gate
until a human explicitly approves or rejects it.

## Autonomous execution boundary

When an agent receives a Feature for autonomous execution:

1. The agent owns the entire Feature scope — all Stories and Tasks within it.
2. The agent creates the `feature/<name>` branch.
3. The agent transitions the Feature to `In Progress` on the GitHub Project board.
4. The agent works through Stories sequentially (or in parallel when safe).
5. The agent creates `story/<name>` branches per Story.
6. The agent transitions each Story to `In Progress` on the board when claimed.
7. The agent self-validates each Task and Story.
8. The agent transitions each Story to `In Review` on the board when ready.
9. The agent requests review at the Story level (WF-006).
10. The agent does **not** approve its own work — review is independent.
11. On Story review approval, the Story transitions to `Done` on the board.
12. On Story PR merge, the Story transitions to `Closed` on the board.
13. When all Stories are Done, the Feature enters integration review (`In Review` on board).
14. The agent does **not** merge to `develop` — that belongs to the human-gated
    `harnessctl merge` step. The agent calls `harnessctl hitl gate HG-MERGE-FEATURE` to create
    the gate, then **pauses** awaiting human approval.
15. On Feature merge to `develop`, the Feature transitions to `Done`, then `Closed` on the
    board.

## GitHub Project synchronization

The GitHub Project board is the operational system of record for work state. The
`.harness/planning/work-breakdown.md` remains the durable planning record.

Every lifecycle transition MUST be reflected on the board:

| Level | Event | Board transition | Responsibility |
|---|---|---|---|
| Feature | Claimed | `Ready → In Progress` | Agent |
| Feature | All Stories done + integ review done | `In Progress → In Review` | Agent |
| Feature | PR merged to develop | `In Review → Done` → `Closed` | Orchestrator / human after gate |
| Story | Branch created | `Ready → In Progress` | Agent |
| Story | Tasks implemented + validated | `In Progress → In Review` | Agent |
| Story | Review approved | `In Review → Done` | Reviewer |
| Story | PR merged to feature | `Done → Closed` | Agent (after merge) |
| Task | Claimed | `Ready → In Progress` | Agent |
| Task | Implementation complete | `In Progress → In Review` | Agent |
| Task | Within Story review | `In Review → Done` | Agent (implicitly via Story) |

See `.harness/agents/go-engineer.md` and `GITHUB_PROJECT_SYNC.md` for the complete
synchronization protocol.

## State reconciliation with GitHub

After any PR, merge, or HITL operation, the workflow MUST reconcile local state against
GitHub:

1. Consult the actual PR state (OPEN / MERGED / CLOSED)
2. Consult the GitHub Issue and Project board status
3. Compare against the expected workflow state
4. If they diverge materially, BLOCK and report the divergence

This prevents the workflow from operating on stale assumptions (e.g., assuming a PR is
still open when it was merged, or assuming a gate is pending when the PR was already
closed).

## What this changes

Previously, the execution boundary was the individual Task: an agent claimed one Task,
implemented it, and handed off. This model elevates the boundary to the Feature:

- **Before:** Agent claims Task → implements → reviews → repeats per Task.
- **Now:** Agent claims Feature → implements all Stories/Tasks → reviews per Story →
  integration review per Feature.

This reduces handoff overhead, preserves context across related Tasks, and aligns the
execution boundary with the branch boundary (`feature/` → `story/`).

## Compatibility

- Task-level claiming is still valid for small, isolated work or when a Feature has only
  one Story with one Task. The Feature is the *default* unit, not the only allowed unit.
- The state machine (Backlog → Ready → In Progress → In Review → Done) applies at every
  level. A Feature has its own lifecycle independent of its children's lifecycles.
- The branching policy (`BRANCHING_POLICY.md`) is the physical realization of this model:
  `feature/` branches are the execution boundary; `story/` branches are the development
  boundary.

## Relationship to workflows

| Workflow | Input | Execution unit | Output |
|---|---|---|---|
| WF-004 Planning | Project Profile + Architecture | Epic → Feature → Story → Task hierarchy | Feature Ready |
| WF-005 Implementation | Ready Feature (or Ready Task for small work) | Feature (creates `feature/` + `story/` branches) | Stories In Review |
| WF-006 Verification | Story In Review (and Feature In Review) | Reviewer per Story, then integration per Feature | Stories Done → Feature Done |
| WF-007 Release | Feature(s) Done on `develop` | Merge `develop` → `main` | Release-ready |

## Scope

This model is generic and applies to all Dedicated Harnesses. No project-specific
execution model is needed unless it extends this with a documented justification.
