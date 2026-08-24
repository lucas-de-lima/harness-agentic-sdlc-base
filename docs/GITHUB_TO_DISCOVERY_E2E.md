# GitHub → Discovery Agent End-to-End

## Goal

Execute the first real end-to-end Agentic SDLC workflow against a GitHub Issue.

## Flow

```text
GitHub Issue: DISCOVERY-001
        ↓
GitHub MCP read
        ↓
Orchestrator
        ↓
Load project specification
        ↓
project-discovery skill
        ↓
Project Profile
        ↓
Profile validation
        ↓
Handoff Packet
        ↓
GitHub execution evidence
        ↓
Issue status → In Review
```

## Boundaries

The Discovery agent may:

- read GitHub work state
- read repository files
- write discovery artifacts
- write bounded execution evidence

It may not:

- implement production code
- choose final architecture
- create dependencies
- create releases
- perform unrelated GitHub mutations

## Success

The end-to-end execution is successful when the work item contains enough evidence to hand the Project Profile to Architecture.
