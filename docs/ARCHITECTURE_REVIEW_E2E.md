# Architecture Review E2E

## Goal

Execute the first complete architecture decision lifecycle:

```text
Discovery
  ↓
Project Profile
  ↓
Architecture Agent
  ↓
Architecture Decision
  ↓
Review Agent
  ├── Approved
  ├── Changes Requested
  └── Blocked
```

## Success condition

The architecture may proceed to implementation planning only when the review outcome is `Approved`.

## Important

A successful architecture review does not authorize implementation by itself.

It authorizes the next workflow: implementation planning.
