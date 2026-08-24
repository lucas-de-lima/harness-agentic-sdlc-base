# Code Review E2E

## Goal

Review the real implementation produced by the Go Engineer E2E.

## Flow

```text
Go Engineer
    ↓
Task In Review
    ↓
Code Review Agent
    ├── Approved
    ├── Changes Requested
    └── Blocked
```

## Success

For the successful path:

- implementation is inspected
- Review Report is produced
- Review Handoff is produced
- Task reaches `Done`
- reviewer makes no source changes
