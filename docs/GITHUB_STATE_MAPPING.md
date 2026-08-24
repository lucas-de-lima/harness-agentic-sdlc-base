# GitHub State Mapping

## Mapping

```text
GitHub Project Status     Workflow State

Backlog                    Backlog
Ready                      Ready
In Progress                In Progress
In Review                  In Review
Blocked                    Blocked
Done                       Done
```

## Rules

A GitHub status is operational state, not proof of completion.

The Orchestrator must validate required gates before setting Done.

## Discovery

Discovery begins from:

`Ready`

and ends at:

`In Review`

for an explicit Discovery work item.

The Architecture workflow consumes the resulting Project Profile after Discovery is accepted.

## Conflict detection

If GitHub says a work item is In Progress but the local execution ledger contains an active execution belonging to another workflow, the Orchestrator must stop and surface the conflict.
