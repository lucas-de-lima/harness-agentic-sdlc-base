# MCP Registry

## Purpose

The registry is the finite catalog of MCP servers approved for the Agentic SDLC.

An MCP is admitted only when a real workflow requires it.

## Initial candidates

### GitHub MCP

Status: adopt existing provider

Reason:
GitHub provides and maintains an official GitHub MCP server. It supports repository, issue, pull-request, Actions, security and other toolsets; toolsets can be selectively enabled. citeturn326995search2turn326995search7

Initial toolsets:

- repos
- issues
- pull_requests

Additional toolsets require demonstrated need.

### Docker

Status: CLI first

Reason:
Docker is deterministic local tooling. Prefer CLI/script invocation unless a future workflow demonstrates a meaningful need for a model-facing structured API.

### Go tooling

Status: CLI first

Use:

- go
- gofmt
- go test
- go vet
- race detector where appropriate
- linter selected by project policy

Do not create a Go MCP solely to wrap standard commands.

### Filesystem

Status: native/runtime first

Do not create a filesystem MCP unless the chosen runtime lacks the required safe capability.

## Approval rule

Every custom MCP needs:

1. use case
2. alternative analysis
3. required tool surface
4. permission model
5. failure behavior
6. maintenance owner
7. versioning strategy
