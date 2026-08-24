# Dedicated Harness Bootstrap Diff Policy

## Expected write set

The first generation should normally touch only:

```text
.harness/**
```

and, when explicitly configured:

```text
docs/architecture/**
docs/project-profile.md
```

## Unexpected changes

Any change outside the expected write set must stop the bootstrap and require inspection.

## Principle

The first Dedicated Harness generation must be easy to review and revert.
