# GitHub Discovery Write Policy

## Allowed writes

The first real workflow may perform only:

1. one execution comment
2. one Project status transition:
   `Ready → In Review`

## Forbidden

- creating new Issues
- deleting Issues
- closing Issues
- editing acceptance criteria
- changing Issue type
- changing parent hierarchy
- changing unrelated Project fields
- repository code mutation through GitHub
- PR creation

## Rationale

This isolates the write path so that any unexpected GitHub mutation is easy to detect.

## Future evolution

After the first E2E cycle is proven, broader controlled writes can be introduced as separate phases.
