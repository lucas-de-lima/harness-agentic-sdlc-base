# Handoff Packet Schema

## Required fields

```yaml
work_item_id:
workflow_id:
agent:
status:
objective:
completed_actions: []
modified_artifacts: []
validation:
  checks: []
  results: []
unresolved_issues: []
risks: []
recommended_next_action:
evidence: []
```

## Discovery-specific requirements

A successful discovery handoff must reference:

- Project Profile
- naming proposal
- evidence sources
- unresolved questions
- repository modification list

## Rule

A handoff cannot claim completion without validation evidence.
