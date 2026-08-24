# Release Gate Model

## Required gates

### Functional

- unit tests pass
- integration tests pass when applicable
- acceptance-critical flows pass

### Build

- reproducible build succeeds
- expected binary/container artifacts exist

### Go quality

- formatting
- `go vet`
- project linter where configured

### Security

- dependency/security checks appropriate to the project
- no secrets in repository
- relevant configuration reviewed

### Runtime

- Docker image builds when containerized
- healthcheck works when defined
- required dependencies start correctly

### Documentation

- README current
- local run instructions current
- configuration documented
- architecture documentation current
- operational notes current

### CI

- default CI pipeline passes
- release workflow, when present, passes its required gates

## Waivers

A skipped gate must have:

- explicit reason
- owner/decision
- scope
- future follow-up when applicable

Do not silently skip.
