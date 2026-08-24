# Codex MCP Commands

## Add the server

```bash
codex mcp add github -- docker run -i --rm -p 127.0.0.1:8085:8085 -e GITHUB_OAUTH_CALLBACK_PORT=8085 -e GITHUB_READ_ONLY=1 -e GITHUB_TOOLSETS=context,issues,projects ghcr.io/github/github-mcp-server
```

Codex supports `codex mcp add` for registering MCP servers in the global Codex configuration. citeturn387937search4turn387937search5

## Inspect

```bash
codex mcp list
codex mcp get github --json
```

## Remove

```bash
codex mcp remove github
```

## Do not use yet

Do not switch to:

```text
GITHUB_READ_ONLY=0
```

and do not enable `all`, write-heavy toolsets, or broad repository mutations during Phase 15.
