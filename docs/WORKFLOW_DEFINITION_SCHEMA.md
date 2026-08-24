# Workflow Definition Schema

## Conceptual YAML

```yaml
id: WF-005
name: implementation
trigger:
  type: github_issue_ready

preconditions:
  - work_item_is_ready
  - required_context_available
  - no_unresolved_blocker

agents:
  - orchestrator
  - go-engineer
  - test-engineer

steps:
  - id: inspect
    action: inspect_repository
  - id: implement
    action: execute_task
  - id: validate
    action: run_required_checks
  - id: handoff
    action: create_review_handoff

gates:
  - build_passes
  - required_tests_pass
  - scope_is_respected

on_failure:
  classify:
    - retryable
    - actionable_defect
    - blocker
    - policy_violation
    - human_decision_required

retry:
  max_attempts: 2

terminal:
  success: In Review
  blocked: Blocked
```

The exact executable format may change when the runtime implementation is built.
