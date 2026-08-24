# Agent Authority Matrix

This matrix defines the default permissions. Project Harnesses may narrow permissions; widening permissions requires explicit justification.

| Role | Decide Requirements | Architecture | Write Production | Write Tests | Review | Security Approval | GitHub Work Mgmt |
|---|---|---|---|---|---|---|---|
| Orchestrator | Coordinate | Escalate | No* | No* | No | No | Yes |
| Discovery | Propose | Propose | No | No | No | No | Limited |
| Architecture | No | Yes | No* | No* | Yes (design) | No | Limited |
| Go Engineer | No | No* | Yes | Yes | No | No | Limited |
| Test Engineer | No | Propose | Limited | Yes | Yes (tests) | No | Limited |
| Reviewer | No | Review | No | No | Yes | No | Limited |
| Security Reviewer | No | Review security impact | No | Security tests only | Yes | Yes within scope | Limited |
| Documentation | No | Record | Docs only | No | No | No | Limited |

* Only when explicitly authorized for a narrowly scoped task.

## Principle

Permission should follow the task, not merely the job title.
