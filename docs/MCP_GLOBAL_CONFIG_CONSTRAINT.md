# MCP Global Configuration Constraint

## Current Codex behavior

Codex configures MCP servers through the user's Codex configuration, currently `~/.codex/config.toml`, with servers declared under `[mcp_servers.<name>]`. The Codex CLI also provides `codex mcp add`, `list`, `get`, and `remove` commands. citeturn697144search1turn387937search4

## Consequence for the layered Harness

The Dedicated Harness does not own a process-local MCP registration.

Instead:

```text
Global Codex MCP registry
        +
Dedicated Harness capability policy
        =
Effective project capability
```

The Dedicated Harness records what the project needs and what agents are authorized to use. The actual server registration is global.

## Safety implication

A globally registered MCP must not automatically imply project-level authorization.

The Base/Dedicated Harness policy remains the authority for whether an agent should use the capability in the current project/workflow.
