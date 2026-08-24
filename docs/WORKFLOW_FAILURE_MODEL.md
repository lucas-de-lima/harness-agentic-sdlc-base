# Workflow Failure Model

## Failure classes

### Retryable

Transient failure likely to succeed without changing the plan.

Examples:
- temporary tool failure
- transient network error
- interrupted command

Action:
- retry within bounded policy

### Actionable defect

The current implementation is wrong or incomplete.

Action:
- return to execution with explicit findings

### Blocker

Progress requires something unavailable.

Examples:
- missing dependency
- unavailable external system
- unresolved requirement

Action:
- move to Blocked

### Policy violation

The agent attempted an action outside its authority or workflow rules.

Action:
- stop workflow
- record violation
- require review

### Human decision required

Evidence is insufficient for a consequential choice, or a Human Gate is pending (see
`HITL_POLICY.md`).

Action:
- stop
- create a Human Gate via `harnessctl hitl gate`
- surface decision request
- do not guess
- workflow PAUSES until the human approves or rejects the gate

## Retry rule

Retries are bounded and step-specific.

Never retry indefinitely.

A retry must preserve the original failure evidence and attempt count.
