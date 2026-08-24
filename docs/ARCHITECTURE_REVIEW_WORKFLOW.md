# Architecture Review Workflow

## Trigger

An Architecture Decision reaches `Architecture Ready` and requires independent review.

## Preconditions

- Architecture Decision exists
- ADR exists
- Project Profile exists
- governing architecture catalog is available
- review skill is available
- no conflicting review execution exists

## Steps

1. Load decision and ADR.
2. Load Project Profile.
3. Load relevant Architecture Catalog and review criteria.
4. Evaluate evidence independently.
5. Classify findings by severity.
6. Produce Review Report.
7. Produce Review Handoff.
8. Transition workflow based on outcome.

## Terminal mapping

### Approved

`Approved`

### Changes Requested

Return producer work to `In Progress`.

### Blocked

Move to `Blocked`.

## Review independence

The reviewer must not ask the original Architect Agent to self-approve.
