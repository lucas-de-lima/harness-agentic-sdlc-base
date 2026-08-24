# Project Input Discovery

## Goal

Determine the actual project boundary before generating a Dedicated Harness.

## Discovery

The Factory must:

1. resolve the Git repository root;
2. inspect top-level files;
3. identify candidate inherited specifications;
4. identify existing agent/runtime instructions;
5. identify project language/tooling;
6. detect whether `.harness/` already exists;
7. record ambiguous inputs.

## Specification selection

Prefer:

1. explicitly configured specification path;
2. a uniquely identifiable root-level project specification;
3. human-selected specification.

Do not arbitrarily choose among multiple plausible specifications.

## Legacy naming

Historical school naming is treated as contextual evidence only.

It must not become the product identity automatically.
