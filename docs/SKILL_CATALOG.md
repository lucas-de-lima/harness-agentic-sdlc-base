# Skill Catalog

## Base Skill Families

### Discovery
- `project-discovery`
- `requirements-extraction`
- `domain-modeling`
- `project-naming`

### Architecture
- `architecture-evaluation`
- `architecture-decision`
- `adr-authoring`
- `dependency-analysis`

### Engineering

Engineering skills are language-specific. The Base Harness provides Go engineering skills built-in.
Project-specific Engineering skills may be created for other technology stacks.

- `idiomatic-go`
- `go-project-structure`
- `go-error-handling`
- `go-http`
- `go-testing`
- `go-concurrency`
- `go-configuration`
- `go-observability`
- `go-performance`

### Infrastructure
- `docker-engineering`
- `ci-engineering`
- `database-integration`

### Quality
- `code-review`
- `test-review`
- `security-review`
- `documentation-review`

## Project Skill Families

Project skills are created only when the base catalog cannot express project-specific knowledge cleanly.

Examples:
- `payments-domain`
- `catalog-domain`
- `game-rules-domain`
- `project-specific-api-contract`
- `project-specific-test-fixtures`

## Skill Selection Principle

The Harness Factory should select the smallest useful set of skills.

More skills do not imply a better agent.

A skill must be added because:
- the workflow requires the capability;
- the project has domain-specific knowledge;
- a quality gate requires it;
- or a known recurring failure warrants it.

## Skill Lifecycle

`proposed -> validated -> active -> deprecated`

Deprecated skills remain documented until no active project depends on them.
