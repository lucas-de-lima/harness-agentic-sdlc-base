# Orchestrator ↔ GitHub Contract

## Purpose

Define the future contract between the Orchestrator and GitHub Projects.

## Source of truth

GitHub owns operational work state.

The Orchestrator owns execution reasoning.

Neither should silently overwrite the other's responsibility.

## Expected capabilities

The GitHub integration should eventually support:

- read issue
- search issues
- create issue
- create sub-issue
- update issue
- update Project fields
- move status
- read parent/sub-issue relationships
- inspect dependencies
- link or inspect pull requests
- add execution comments
- close completed work

## Permission principle

Read capabilities should be broadly available.

Write capabilities should be limited by agent role.

Destructive capabilities should require explicit policy authorization.

## Execution pattern

```text
GitHub Work Item
      ↓
Orchestrator reads state
      ↓
Agent receives bounded task
      ↓
Agent changes repository
      ↓
Validation
      ↓
Orchestrator records result
      ↓
GitHub state transition
```

## Important

GitHub is not the place to store the entire agent context.

The issue should contain enough information to understand the work item and acceptance criteria. Detailed project knowledge remains in the repository's durable documents and dedicated harness.
