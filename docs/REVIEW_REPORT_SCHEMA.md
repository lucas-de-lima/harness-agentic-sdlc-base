# Review Report Schema

## Required fields

```yaml
work_item_id:
workflow_id:
execution_id:
reviewer:
artifact:
decision:
summary:
findings:
  - severity:
    category:
    finding:
    evidence:
    recommendation:
gates:
  - name:
    result:
    evidence:
residual_risks: []
next_action:
```

## Valid decisions

- `Approved`
- `Changes Requested`
- `Blocked`

## Evidence

Every Blocking or Major finding must include evidence.

A reviewer may not reject based solely on preference.
