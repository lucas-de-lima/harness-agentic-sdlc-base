# Code Review E2E Execution

## Preconditions

- Task is `In Review`
- Implementation Handoff exists
- actual diff exists
- architecture is approved
- code-review skill is available
- no conflicting review execution exists

## Execution

1. Load Task.
2. Load acceptance criteria.
3. Load implementation handoff.
4. Inspect repository status and diff.
5. Inspect changed production code.
6. Inspect changed tests.
7. Validate relevant Go checks.
8. Review architecture impact.
9. Review obvious security risks.
10. Produce Review Report.
11. Produce Review Handoff.
12. Apply only the permitted GitHub state transition.
13. Stop.

## Evidence

The evidence must prove that the decision came from inspecting the real implementation.
