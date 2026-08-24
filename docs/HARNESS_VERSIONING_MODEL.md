# Harness Versioning Model

## Purpose

Define how a Dedicated Harness evolves independently while remaining derived from the Base Harness.

## Source relationships

Each Dedicated Harness records:

- Base Harness version
- generated-at revision
- project harness version

Example:

```text
base: 0.7.0
harness: 0.1.0
```

## Independence

The Dedicated Harness is committed to the project's Git repository.

Future Base Harness updates do not automatically rewrite project harnesses.

## Upgrade model

A future upgrade workflow may:

1. compare Base and Dedicated versions
2. detect applicable changes
3. propose updates
4. generate a migration plan
5. apply approved changes
6. validate the resulting harness

## Principle

Generation is not synchronization.

A project harness becomes project-owned once committed.
