# Orchestrator Discovery Workflow

## Trigger

A project enters Discovery with an inherited project specification.

## Preconditions

- repository root is known
- specification exists
- discovery skill is available
- output path is writable
- no conflicting discovery lock exists

## Steps

1. Resolve repository boundary.
2. Load project specification.
3. Load Dedicated/Base Harness instructions that apply.
4. Invoke `project-discovery`.
5. Collect Project Profile.
6. Validate Project Profile.
7. Create Handoff Packet.
8. Record execution evidence.
9. Transition workflow to its terminal state.

## Terminal states

### Success

`Discovery Complete`

### Blocked

`Discovery Blocked`

### Failed

`Discovery Failed`

## Boundedness

The Orchestrator may perform one discovery attempt and a bounded retry when validation reveals a correctable output defect.

It must not loop indefinitely.
