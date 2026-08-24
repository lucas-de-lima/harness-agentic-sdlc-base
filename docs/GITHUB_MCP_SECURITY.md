# GitHub MCP Security

## Phase 15 security posture

Read-only only.

The official GitHub MCP server documents `--read-only` / `GITHUB_READ_ONLY=1` as a mode that prevents modifications to repositories, issues, pull requests, and similar resources. citeturn252943search0

## Authentication

Prefer the official OAuth flow for interactive local use when practical. GitHub states that local stdio OAuth uses PKCE and keeps the resulting token in memory; Docker requires the callback port to be published to loopback. citeturn726420search5

Alternative:

- Personal Access Token with minimum required permissions
- never commit tokens
- never put secrets into the repository

## Tool minimization

The initial toolset is:

```text
context
issues
projects
```

No `all`.

No repository write tools.

No pull-request mutation.

No Actions mutation.

## Codex approval

MCP capability and Codex action approval remain separate controls.

A read-only GitHub MCP reduces what the external server can do; Codex's own approval/sandbox settings govern local execution and edits. Current Codex guidance distinguishes read-only, auto, and full-access approval modes. citeturn387937search5
