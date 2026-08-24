# GitHub MCP Validation

## Layer 1 — configuration

```bash
codex mcp list
codex mcp get github --json
```

Verify:

- server exists
- enabled
- stdio transport
- Docker command present

## Layer 2 — server

The server must expose the intended tool surface.

Expected families:

- context
- issues
- projects

Write tools must not be available while read-only mode is active. GitHub documents that read-only mode filters write tools. citeturn252943search0

## Layer 3 — identity

Use a harmless read-only request in Codex:

- identify the authenticated GitHub user
- list repositories the identity can see
- read a known Issue
- read a known Project

Do not create, update, delete, or comment on anything.

## Layer 4 — project policy

The Dedicated Harness must state which GitHub capabilities the current project/workflow is authorized to use.

A global server being present is not sufficient authorization.

## Failure handling

If unexpected write tools appear:

1. stop
2. remove/disable the server
3. inspect toolset and read-only configuration
4. do not proceed to write-enabled mode
