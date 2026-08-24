# Go Engineer Change Boundary

## Allowed

- production code related to the Task
- tests related to the Task
- local configuration directly required by the Task
- implementation documentation when the change creates durable knowledge

## Requires escalation

- architecture changes
- new infrastructure not anticipated by planning
- new external service
- significant dependency change
- schema migration outside planned scope
- broad refactor unrelated to the Task
- requirement contradiction

## Forbidden

- opportunistic cleanup of unrelated code
- mass formatting outside the relevant scope
- speculative abstractions
- unrelated dependency upgrades
- deleting unrelated features
