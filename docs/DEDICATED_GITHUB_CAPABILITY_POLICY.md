# Dedicated GitHub Capability Policy

## Example

```yaml
github:
  server: github
  capabilities:
    context: read
    issues: read
    projects: read
  workflows:
    discovery:
      allowed: true
      mutations: false
    implementation:
      allowed: false
    review:
      allowed: false
```

This policy is declarative. It does not override the global Codex MCP registration.

The Orchestrator must evaluate the policy before invoking GitHub capabilities.
