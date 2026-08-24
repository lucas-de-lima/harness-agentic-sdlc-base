# Custom MCP Design Standard

Custom MCP servers are justified only when an existing capability is insufficient.

## Required design

Every custom MCP must document:

- purpose
- consumers
- tools
- input schemas
- output schemas
- error semantics
- authorization
- auditability
- version
- transport
- operational dependencies
- test strategy

## Tool design rules

Tools should be:

- narrow
- deterministic where possible
- explicit about side effects
- idempotent where practical
- bounded in resource use
- safe to retry when practical

## Side effects

A mutating tool should make side effects obvious from its name and schema.

Examples:

Good:
- `create_project_issue`
- `update_project_status`

Bad:
- `manage_github`

## Current protocol baseline

Target MCP 2026-07-28 unless a project has a documented compatibility requirement. The specification now has stronger authorization semantics and a stateless protocol core. citeturn326995search0
