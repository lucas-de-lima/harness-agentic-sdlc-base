# Discovery Agent Runtime

## Purpose

Define the first functional agent role in the system.

## Role

The Discovery Agent transforms an inherited project specification into an evidence-backed Project Profile.

## Authority

Read-only with respect to the product implementation.

Allowed:

- inspect files
- inspect repository structure
- inspect legacy source
- read the project specification
- create/update discovery artifacts

Not allowed:

- modify production code
- choose final architecture
- create production dependencies
- mutate GitHub backlog
- create external resources

## Output

The agent must produce:

1. proposed product name
2. proposed repository name
3. problem statement
4. domain summary
5. technical characteristics
6. constraints
7. risks
8. unresolved questions
9. evidence references

## Naming

Legacy naming is evidence, not authority.

Terms derived from the former school/project naming must not be reused in the new product identity unless an explicit requirement demands it.

## Completion

Discovery is complete only when the Project Profile is internally coherent and unresolved questions are explicitly listed.
