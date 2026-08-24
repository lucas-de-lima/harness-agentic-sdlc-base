# MCP Permission Model

## Purpose

Prevent agents from receiving more external authority than their role requires.

## Permission tiers

### Read

Examples:

- list repositories
- read issue
- read Project state
- inspect pull request

### Write

Examples:

- create issue
- update Project field
- add comment
- create branch

### Destructive

Examples:

- delete repository content
- close/delete external resources
- force destructive state changes

Destructive capabilities are disabled by default.

## Agent policy

### Discovery

Prefer read-only access.

### Architect

Read GitHub state. Write architecture-related issues only when explicitly part of the workflow.

### Developer

Read work state and write the project artifacts. GitHub write operations should be limited to task-state and execution evidence.

### Reviewer

Read-only by default. May add review findings.

### Orchestrator

May perform controlled workflow-state mutations.

### Merge (special restricted capability)

Merge is **not** a standard agent capability. All merges are performed exclusively through
`harnessctl merge`, which enforces HITL gate checking before executing the merge.

Agents must never be configured with `GITHUB_TOOLSETS=pull_requests` in their MCP profile,
because this toolset includes `github_merge_pull_request`. Instead, use the toolset
configuration documented in `GITHUB_MCP_SECURITY.md` and `.vscode/mcp.json`.

## Principle

Repository write access and GitHub write access are separate authorities.

An agent may be allowed to modify code without being allowed to mutate the backlog arbitrarily.
