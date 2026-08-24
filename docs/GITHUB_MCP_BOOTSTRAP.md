# GitHub MCP Bootstrap

## Goal

Configure the official GitHub MCP Server in Codex using Docker, initially in read-only mode.

GitHub's official server supports Docker execution, selectable toolsets, and a read-only mode that removes mutation tools. citeturn726420search2turn252943search0

## Initial capability set

Expose only:

- `context`
- `issues`
- `projects`

Do not enable repository mutation, pull requests, Actions, security, or other toolsets yet.

GitHub's local server supports a `projects` toolset, while `projects` is not part of the default toolset, so it must be explicitly enabled. citeturn394357search0turn394357search1

## Docker authentication

The official local server supports OAuth on github.com. In Docker, the OAuth callback must use a fixed port published only to loopback. GitHub documents port 8085 for this flow. citeturn726420search0turn726420search5

## Recommended first configuration

Use `GITHUB_READ_ONLY=1` and:

`GITHUB_TOOLSETS=context,issues,projects`

This creates a deliberately narrow read-only GitHub capability.

## Important

The GitHub MCP image is external infrastructure. Pinning an exact image release should be considered before using the system unattended. For the first interactive bootstrap, use the official image and validate the server/tool inventory.

## First validation

Run:

```bash
codex mcp list
codex mcp get github --json
```

Then open Codex and verify the GitHub tools are available.

## Expected result

The GitHub server appears as enabled, and only the expected read-only GitHub capabilities are available to the runtime.
