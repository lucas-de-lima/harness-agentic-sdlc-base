# Code Review Workflow

## Trigger

Implementation reaches `In Review`.

## Preconditions

- implementation handoff exists
- Task exists
- acceptance criteria exist
- approved architecture exists
- code changes exist
- review skill available
- no conflicting review execution

## Steps

1. Read Task and acceptance criteria.
2. Read Implementation Handoff.
3. Inspect Git diff and changed files.
4. Inspect relevant tests.
5. Read architecture/ADR constraints.
6. Run targeted validation when required.
7. Classify findings.
8. Produce Review Report.
9. Produce Review Handoff.
10. Transition the Task.

## Outcomes

### Approved
`In Review → Done`

### Changes Requested
`In Review → In Progress`

### Blocked
`In Review → Blocked`

The reviewer does not modify implementation files.
