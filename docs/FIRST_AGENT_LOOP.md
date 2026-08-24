# First Agent Loop

## Goal

Prove the first bounded agentic workflow end-to-end without granting destructive authority.

## Flow

```text
Work Item
   ↓
Orchestrator
   ↓
Discovery Agent
   ↓
Project Profile
   ↓
Validation
   ↓
Handoff
   ↓
Workflow terminal state
```

## Scope

The first loop is discovery-only.

The agent may inspect the repository and write discovery artifacts, but must not:

- change production source
- choose final architecture
- mutate GitHub
- create external resources
- install dependencies

## Success

The loop is successful when a valid Project Profile and Handoff Packet are produced and all required guards pass.
