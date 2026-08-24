# MCP & Tooling Architecture

## Purpose

Define when a capability belongs to the agent host, a local CLI/script, an MCP server, or an external integration.

## Decision order

Use the least sophisticated integration that provides the required capability:

1. Native agent capability
2. Existing CLI/tool
3. Local script
4. Existing MCP server
5. Custom MCP server
6. External service integration

Custom MCP is the last practical option, not the default.

## Capability classes

### Native capability

Use for reasoning, file inspection/editing, command execution, and other capabilities already supplied reliably by the agent runtime.

### CLI or script

Use for deterministic local operations such as:

- Go formatting/build/test
- static checks
- Docker commands
- repository-local automation
- deterministic validation

Scripts should be preferred over MCP when no model-facing discovery or abstraction benefit exists.

### MCP

Use when the agent needs structured access to an external or reusable capability and direct CLI/script access is insufficient.

Good candidates:

- GitHub Projects and Issues
- reusable external systems
- specialized structured domain tools

### External integration

Use when the capability is inherently provided by a remote service.

## MCP design rule

An MCP server should expose a small, task-oriented surface.

Do not mirror an entire platform unless the workflow actually needs it.

## Versioning

The Harness Base must record the MCP specification version targeted by its MCP implementations.

The current MCP specification is 2026-07-28. It introduced a stateless protocol core, stronger authorization, cache hints for list results, and a formal extension/deprecation model. Custom servers must not silently target an incompatible revision. citeturn326995search0turn326995search1
