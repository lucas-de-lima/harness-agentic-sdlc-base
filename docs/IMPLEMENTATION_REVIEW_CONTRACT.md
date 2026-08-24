# Implementation Review Contract

## Separation

The Go Engineer produces an implementation.

A separate Reviewer evaluates it.

The Engineer may self-check, but self-check is not approval.

## Review levels

Review happens at two levels (see `FEATURE_EXECUTION_MODEL.md`):

### Story-level review

The Reviewer evaluates one User Story's implementation:

- Story
- acceptance criteria
- implementation diff (`story/<name>` vs `feature/<name>`)
- tests and results
- Story implementation handoff
- approved architecture
- relevant ADRs

Outcome: Approved → merge `story/<name>` → `feature/<name>`, Story Done.
         Changes Requested → Story In Progress.
         Blocked → Story Blocked.

### Feature-level integration review

When all Stories are Done, the Reviewer evaluates the Feature as a whole:

- Feature
- all Story review outcomes
- integration diff (`feature/<name>` vs `develop`)
- integration test results
- Feature implementation handoff
- approved architecture

Outcome: Approved → merge `feature/<name>` → `develop`, Feature Done.
         Changes Requested → Feature In Progress (remediate affected Stories).
         Blocked → Feature Blocked.

## Reviewer receives

- Feature (for integration review) or Story (for Story review)
- acceptance criteria
- implementation diff
- tests and results
- implementation handoff
- approved architecture
- relevant ADRs

## Reviewer outcome

- Approved
- Changes Requested
- Blocked

## Engineer cannot

- approve its own Story or Feature
- close a Story or Feature as Done
- override a review finding
