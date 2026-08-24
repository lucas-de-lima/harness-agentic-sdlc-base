# Architecture Review E2E Workflow

## Trigger

`Architecture Ready`

## Preconditions

- Architecture Decision exists
- ADR exists
- Project Profile exists
- Architecture Review Agent is available
- architecture review criteria are available
- no conflicting review execution exists

## Steps

1. Load Architecture Decision.
2. Load ADR.
3. Load Project Profile.
4. Load governing architecture documents.
5. Run independent review.
6. Validate Review Report.
7. Produce Review Handoff.
8. Transition according to review result.
9. If Approved, create the downstream implementation-planning trigger.
10. Do not implement code.

## Outcome mapping

```text
Approved
    ↓
Architecture Approved

Changes Requested
    ↓
In Progress

Blocked
    ↓
Blocked
```
