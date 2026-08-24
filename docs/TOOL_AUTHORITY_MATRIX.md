# Tool Authority Matrix

| Agent | Files | Git | GitHub Read | GitHub Write | GitHub Merge | Docker | Go CLI | External |
|---|---|---|---|---|---|---|---|---|---|---|
| Orchestrator | Read | Read | Yes | Controlled | **FORBIDDEN** | Limited | Limited | No by default |
| Discovery | Read | Read | Yes | No | **FORBIDDEN** | No | Limited | No |
| Architect | Read | Read | Yes | Controlled | **FORBIDDEN** | No | Read/validate | No |
| Go Engineer | Read/Write | Controlled | Yes | Task-scoped | **FORBIDDEN** | Yes | Yes | Project-specific |
| Test Engineer | Read/Write tests | Controlled | Yes | Test evidence only | **FORBIDDEN** | Yes | Yes | Project-specific |
| Reviewer | Read | Read | Yes | Findings/comments | **FORBIDDEN** | No | Yes | No |
| Security Reviewer | Read | Read | Yes | Findings/comments | **FORBIDDEN** | Limited | Yes | No |
| Documentation | Read/Write docs | Controlled | Yes | Documentation evidence | **FORBIDDEN** | No | Limited | No |

## Interpretation

"Controlled" means policy-constrained by workflow and task scope.
"FORBIDDEN" means the agent must never directly invoke the merge operation. The only authorized
merge path is `harnessctl merge`, which enforces HITL gate checking before executing the merge.

No agent gets unrestricted access merely because its role is trusted.
