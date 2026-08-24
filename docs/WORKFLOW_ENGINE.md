# Workflow Engine

## Purpose

Define the executable workflow model for the Agentic SDLC.

The workflow engine coordinates agents and tools against an explicit work item and state.

## Core model

```text
Trigger
  ↓
Preconditions
  ↓
Load Context
  ↓
Plan/Deliberate
  ↓
Execute
  ↓
Validate
  ↓
Handoff/Review
  ↓
Transition State
  ↓
Record Evidence
```

A workflow must have an explicit terminal condition.

## Workflow properties

Every workflow defines:

- identifier
- purpose
- trigger
- inputs
- preconditions
- allowed agents
- allowed tools
- steps
- validation gates
- state transitions
- failure behavior
- retry policy
- terminal conditions

## Principle

A workflow is a bounded process, not an autonomous loop.

The engine must stop when:

- the objective is complete
- a required decision cannot be safely made
- a blocker is detected
- a policy violation occurs
- retry limits are exhausted
- human intervention is required
