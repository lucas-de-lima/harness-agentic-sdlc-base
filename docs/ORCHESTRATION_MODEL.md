# Orchestration Model

## Principle

The Orchestrator controls flow, not implementation style.

## Execution unit

The default unit of autonomous execution is the **Feature** (see
`FEATURE_EXECUTION_MODEL.md`). The Orchestrator assigns a Feature to an agent; the agent
works through the Feature's Stories and Tasks autonomously, creating branches and requesting
review per Story.

For small, isolated work, the Orchestrator may assign a single Task. This is the exception,
not the default.

## Basic Loop

1. Read current project state.
2. Identify the next Ready Feature (or Ready Task for small work).
3. Select the smallest qualified agent.
4. Provide the Feature scope: Stories, Tasks, acceptance criteria, dependencies, architecture.
5. Receive an explicit handoff (per Story or per Feature).
6. Validate completion against the relevant gate.
7. Route to review, remediation, or the next phase.

## Routing Rules

- Discovery before architecture when requirements are unclear.
- Architecture before implementation when architectural intent is unresolved.
- Per-Story review after each Story's implementation.
- Feature-level integration review after all Stories are Done.
- Security review when a change affects authentication, authorization, secrets, external input, dependencies, network exposure, or sensitive data.
- Documentation after stable decisions, not after every trivial edit.

## Failure Loop

If review fails (per Story):

```text
Implement Story → Review → Reject → Remediate → Review
```

If integration review fails (per Feature):

```text
Feature In Review → Reject → Remediate (per affected Story) → Review
```

Do not automatically restart the entire workflow.

## Architecture Change

If implementation reveals that the approved architecture is insufficient:

```text
Implementation
   ↓
Escalation
   ↓
Architecture Agent
   ↓
ADR / decision
   ↓
Implementation continues
```

The implementation agent must not silently redesign the system.
