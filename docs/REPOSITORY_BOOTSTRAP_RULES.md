# Repository Bootstrap Rules

## Purpose

Define what the Harness Factory must create when initializing a product repository.

## Required

- Git repository
- project README
- Dedicated Harness
- Go module
- architecture documentation
- project task-tracking linkage
- baseline validation commands

## Conditional

- `cmd/`
- `internal/`
- `pkg/`
- `tests/`
- `Dockerfile`
- `compose.yaml`
- database
- CI workflows

These are selected by the architecture and project needs.

## Forbidden by default

- empty packages created for symmetry
- generic `pkg/` when nothing is publicly reusable
- placeholder microservices
- unused Docker services
- generated documentation that duplicates GitHub
