# Architecture E2E Workflow

## Trigger

A Discovery work item has reached `In Review` and its Project Profile has passed validation.

## Preconditions

- Project Profile exists
- Discovery Handoff Packet exists
- Architecture Agent skill is available
- Architecture catalog is available
- no conflicting architecture execution exists

## Steps

1. Read Project Profile.
2. Read Discovery evidence and unresolved questions.
3. Identify simplest viable architecture.
4. Identify plausible alternatives.
5. Compare candidates.
6. Select architecture.
7. Produce Architecture Decision.
8. Produce ADR.
9. Validate decision output.
10. Produce Architecture Handoff.

## Terminal states

- Success: `Architecture Ready`
- Blocked: `Architecture Blocked`
- Failure: `Architecture Blocked`

## Retry

At most two bounded attempts for correctable output defects.
