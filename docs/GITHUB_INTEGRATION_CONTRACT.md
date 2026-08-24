# GitHub Integration Contract

## Purpose

Define the first operational contract between the Agentic SDLC and GitHub.

## Responsibility split

GitHub owns:

- issue identity
- issue hierarchy
- Project membership
- operational status
- issue comments and linked evidence
- pull-request relationships

The Orchestrator owns:

- interpreting work state
- selecting the next bounded workflow
- invoking agents
- validating outcomes
- deciding whether a workflow can transition

## Read path

The Orchestrator may read:

- issue title/body
- issue type
- labels
- parent/sub-issue relationships
- Project fields needed by the workflow
- comments relevant to execution
- linked pull requests

GitHub Projects exposes issue-type, parent/sub-issue, and sub-issue-progress fields. citeturn501381search0turn501381search4

## Write path

Phase 14 write operations are intentionally limited to:

- add execution comment
- update workflow status field when authorized
- add/link execution evidence

No repository deletion, issue deletion, or destructive project operations are permitted.

## Source of truth

GitHub remains the operational work-state source.

The Execution Ledger remains the execution audit/evidence record.
