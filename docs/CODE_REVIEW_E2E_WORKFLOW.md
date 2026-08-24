# Code Review E2E Workflow

## Goal

Validate the complete implementation lifecycle using the real code produced by the Go Engineer.

## Flow

```text
Task In Review
      ↓
Code Review Agent
      ↓
Review Report
      ↓
Approved / Changes Requested / Blocked
```

## Approved path

```text
In Review
   ↓
Approved
   ↓
Done
```

`Done` is only reached by the review workflow.

## Changes Requested

```text
In Review
   ↓
Changes Requested
   ↓
In Progress
   ↓
Go Engineer
   ↓
In Review
   ↓
Code Review
```

## Blocked

```text
In Review
   ↓
Blocked
```

## Constraints

The reviewer does not modify implementation files.

The reviewer does not alter acceptance criteria.

The reviewer does not perform architecture changes.
