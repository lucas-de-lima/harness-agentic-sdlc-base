# Dedicated Harness Bootstrap

## Purpose

Create the first project-owned Dedicated Harness from a real project repository.

## Inputs

- target project root
- inherited project specification
- Base Harness version
- validated Project Profile
- approved Architecture Decision
- selected Base capabilities

## Output

A `.harness/` directory committed inside the product repository.

## Bootstrap order

```text
Target project
    ↓
Repository discovery
    ↓
Project Profile
    ↓
Naming proposal
    ↓
Architecture deliberation
    ↓
Capability selection
    ↓
Dedicated Harness generation
    ↓
Validation
    ↓
Human review
    ↓
Git commit
```

## Important

The first bootstrap should support a staged mode:

1. discovery-only
2. proposal
3. generation
4. validation

It should not silently commit or push changes.

## Project ownership

Once generated and committed, the Dedicated Harness belongs to the product repository.

Base Harness upgrades are proposals, not automatic rewrites.
