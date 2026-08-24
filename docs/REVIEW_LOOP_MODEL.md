# Review Loop Model

## Normal path

```text
Architect
   ↓
Review
   ↓
Approved
```

## Correction path

```text
Architect
   ↓
Review
   ↓
Changes Requested
   ↓
Architect
   ↓
Review
```

## Blocked path

```text
Architect
   ↓
Review
   ↓
Blocked
   ↓
Human / upstream decision
```

## Retry policy

The Review Agent is not an infinite critic.

Only explicit corrections should create another architecture iteration.
