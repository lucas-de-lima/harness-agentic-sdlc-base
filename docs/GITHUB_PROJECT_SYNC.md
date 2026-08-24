# GitHub Project Synchronization Policy

## Purpose

Define the mandatory synchronization protocol between workflow execution state and the
GitHub Project board. The GitHub Project is the operational system of record; the
`.harness/planning/work-breakdown.md` is the durable planning record.

## Principle

The GitHub Project board reflects real-time execution state. Every meaningful lifecycle
transition must be reflected on the board before the next step begins.

## Data ownership

| Artifact | Owns | Example |
|---|---|---|
| GitHub Project | Operational state | Status = "In Progress", Priority = "P1" |
| GitHub Issue | Work item definition | Acceptance criteria, type, hierarchy |
| `.harness/planning/work-breakdown.md` | Durable planning | Dependency graph, risk analysis |
| `.harness/hitl/gates.json` | Human gate audit | approvals, rejections, merge origins |

## Lifecycle transitions

### User Story

```text
Backlog → Ready → In Progress → In Review → Done → Closed
```

| Transition | Trigger | Who |
|---|---|---|
| Ready → In Progress | Agent creates `story/<name>` branch | go-engineer |
| In Progress → In Review | All Tasks implemented + validation passes | go-engineer |
| In Review → Done | Review approves (WF-006) | reviewer |
| Done → Closed | Story PR merged to `feature/<name>` | agent (after merge detection) |

### Feature

```text
Backlog → Ready → In Progress → In Review → Done → Closed
```

| Transition | Trigger | Who |
|---|---|---|
| Ready → In Progress | First story branch is created | go-engineer |
| In Progress → In Review | All Stories Done + integration validation | go-engineer |
| In Review → Done | Feature PR merged to `develop` | Orchestrator / human |
| Done → Closed | After merge detection + gate satisfaction | Orchestrator |

### Task

```text
Backlog → Ready → In Progress → In Review → Done
```

| Transition | Trigger | Who |
|---|---|---|
| Ready → In Progress | Agent claims the Task | go-engineer |
| In Progress → In Review | Task implementation + validation | go-engineer |
| In Review → Done | Implicit via Story review | reviewer |

## Synchronization commands

Use `gh project item-edit` to update board fields:

```bash
# Get project number and item ID
GH_PROJECT=$(gh project list --owner <owner> --json number --jq '.[0].number')
ISSUE_NODE_ID=$(gh issue view <number> --json id --jq '.id')

# Set status
gh project item-edit --project "$GH_PROJECT" --id "$ISSUE_NODE_ID" \
  --field Status --value "In Progress"
```

## State reconciliation

After any PR, merge, or HITL operation, the workflow MUST:

1. Query the actual PR state (OPEN / MERGED / CLOSED) via `gh pr view <number> --json state`
2. Query the GitHub Issue and its Project board fields
3. Compare against the expected workflow/gate state
4. If divergences are material (e.g., PR merged but gate still pending), call
   `harnessctl hitl reconcile` to diagnose and resolve

## What is preserved during synchronization

- Issue type (Epic / Feature / User Story / Task)
- Status (Backlog / Ready / In Progress / In Review / Blocked / Done)
- Priority (P0 / P1 / P2 / P3)
- Effort (XS / S / M / L / XL)
- Phase (Discovery / Architecture / Planning / Implementation / Verification / Release)
- Risk (Low / Medium / High)
- Parent/sub-issue relationships

No field should be cleared or reset to default during synchronization.

## Prohibited

- Setting `Done` or `Closed` on the board before the work is technically complete
- Closing GitHub Issues via automation before the corresponding merge is confirmed
- Silently modifying issue hierarchy (parent, type) during synchronization
- Using board synchronization as a substitute for HITL gates

## Relationship to other policies

- `HITL_POLICY.md` — gates are the authority for merge decisions, not board state
- `FEATURE_EXECUTION_MODEL.md` — board sync is part of the autonomous execution flow
- `GITHUB_STATE_MAPPING.md` — defines valid Status values and their workflow meaning
- `PROJECT_AUTOMATION_POLICY.md` — automation boundaries for project field updates