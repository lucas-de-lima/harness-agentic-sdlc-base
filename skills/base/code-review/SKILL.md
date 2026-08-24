---
name: code-review
description: Independently review a Go implementation in In Review state against the Task, acceptance criteria, approved architecture, tests, Go engineering standards, and relevant security expectations. Approve, request changes, or block without modifying the implementation.
---

# Code Review

## Purpose

Determine whether the implementation is ready to be accepted.

## Inputs

- GitHub Task
- acceptance criteria
- Implementation Handoff
- actual Git diff
- changed source files
- changed tests
- approved architecture
- relevant ADRs
- Go engineering standards

## Procedure

1. Read the Task completely.
2. Read acceptance criteria.
3. Read the Implementation Handoff.
4. Inspect git status.
5. Inspect the actual diff.
6. Inspect all changed files.
7. Review tests and failure-path coverage.
8. Check architecture alignment.
9. Check obvious security concerns.
10. Check unnecessary complexity or risky abstractions.
11. Classify findings.
12. Produce Review Report.
13. Choose Approved, Changes Requested, or Blocked.

## Independence rule

Do not accept the Engineer's conclusion without inspecting evidence.
Do not reject merely because you personally prefer a different implementation.

## Read-only rule

Do not modify source code, tests, configuration, architecture, or the Task.

## Approval

Approve only when no Blocking or unresolved Major defect remains and all required acceptance gates have evidence.

## Next state

Approved -> Done
Changes Requested -> In Progress
Blocked -> Blocked
