# Workflow Handoff Model

## Purpose

Define what one agent must provide before another agent continues.

## Handoff packet

Every handoff contains:

- work item identifier
- objective
- completed actions
- modified artifacts
- validation performed
- validation results
- unresolved issues
- risks
- recommended next action
- current state

## Rule

A receiving agent must not infer missing completion evidence from the fact that a previous agent stopped.

The handoff is explicit evidence.

## Rejection

A reviewer may return a handoff when:

- required evidence is missing
- implementation violates scope
- quality gates fail
- architecture is contradicted
- acceptance criteria are unmet
