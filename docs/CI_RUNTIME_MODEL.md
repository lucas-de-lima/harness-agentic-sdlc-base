# CI Runtime Model

## Purpose

Define the expected CI baseline without prescribing unnecessary pipeline complexity.

## Baseline stages

```text
format/check
    ↓
unit tests
    ↓
build
    ↓
integration tests (when applicable)
    ↓
security/quality checks
```

## Pull requests

A pull request should provide enough automated evidence for reviewers to determine whether the change meets its required gates.

## Release

Release workflows are introduced only when the project has a meaningful release artifact.

## Project-specific additions

A Dedicated Harness may add:

- database service
- containerized integration environment
- contract tests
- benchmarks
- race detection
- generated artifact checks

Only when justified by the architecture and requirements.
