# Implementation Rollback Policy

## Purpose

Keep the first autonomous implementation easy to recover.

## If the agent fails before handoff

The user may discard the branch/worktree changes or reset using normal Git procedures after reviewing the diff.

The workflow itself must preserve failure evidence.

## If tests fail

Keep the Task `In Progress` while the agent can correct a bounded implementation defect.

## If architecture conflict is discovered

Stop implementation and return the Task to a controlled planning/architecture decision path.

Do not conceal the conflict by changing the architecture inside the implementation workflow.

## If unrelated files were changed

Stop and inspect the diff before any further action.
