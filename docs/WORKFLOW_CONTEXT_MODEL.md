# Workflow Context Model

## Context layers

```text
Base Constitution
    ↓
Dedicated Harness
    ↓
GitHub Work Item
    ↓
Relevant durable project knowledge
    ↓
Current repository state
    ↓
Current execution evidence
```

Only relevant context should be loaded.

## Context budget principle

More context is not automatically better.

The Orchestrator should provide the minimum sufficient context for each agent and task.

## Required execution context

A task execution should identify:

- repository
- work item
- current state
- objective
- acceptance criteria
- relevant files/areas
- applicable skills
- tool permissions
- previous attempt evidence
