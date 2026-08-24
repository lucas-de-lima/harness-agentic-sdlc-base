# Docker Runtime Model

## Purpose

Define the role of Docker in the product repositories.

## Principle

Docker provides reproducible execution and integration environments. It does not replace the native Go toolchain for every local action.

## Required baseline

When applicable, a product repository should provide:

- Dockerfile
- compose.yaml
- reproducible environment variables/configuration
- healthcheck strategy
- local development instructions

## Use Docker for

- service dependencies
- integration tests
- reproducible runtime
- databases and external infrastructure required by the project
- environment parity

## Use native tooling for

- fast unit tests
- formatting
- static checks
- local iteration

The project should expose a consistent command interface, such as:

```text
make test
make lint
make build
make run
make integration
```

The exact targets are project-specific.

## No infrastructure theater

Do not introduce containers for services that the application does not need.
