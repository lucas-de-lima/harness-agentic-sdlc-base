# Go Engineer E2E Workflow

## Preconditions

- Task type = `Task`
- status = `Ready`
- architecture = `Approved`
- planning = `Ready`
- dependencies = resolved
- repository = correct product repository
- go-engineer skill = available
- no conflicting implementation execution

## Steps

1. Read the Task and acceptance criteria.
2. Read architecture and relevant ADRs.
3. Inspect repository state.
4. Claim Task:
   `Ready → In Progress`
5. Implement smallest correct change.
6. Run relevant tests and Go quality checks.
7. Inspect final diff.
8. Produce Implementation Handoff.
9. Add bounded execution evidence.
10. Transition:
   `In Progress → In Review`
11. Stop.

## Forbidden

Do not:

- mark Done
- approve code review
- change architecture
- create unrelated work
- perform unrelated GitHub writes
