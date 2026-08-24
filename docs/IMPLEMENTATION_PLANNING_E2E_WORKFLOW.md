# Implementation Planning E2E Workflow

## Trigger

`Architecture Approved`

## Preconditions

- Project Profile valid
- Architecture Decision approved
- Review Report approved
- GitHub Project available
- planner skill available
- no conflicting planning execution

## Steps

1. Read approved Architecture Decision.
2. Read Project Profile.
3. Read Review Report and residual risks.
4. Identify the major product/system outcome.
5. Create Epic.
6. Create Features.
7. Create User Stories.
8. Create concrete Tasks.
9. Add acceptance criteria.
10. Add material dependencies.
11. Assign priority, effort, phase, and risk.
12. Keep new work in `Backlog`.
13. Validate planning completeness.
14. Move only the first executable Task to `Ready`.
15. Create planning evidence.
16. Stop.

## Terminal state

`Planning Ready`

## Failure

`Planning Blocked`

## Important

The Planner does not begin implementation.
