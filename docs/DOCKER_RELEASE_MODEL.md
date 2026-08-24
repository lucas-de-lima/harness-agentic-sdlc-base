# Docker Release Model

## Purpose

Define the minimum runtime checks for containerized projects.

## Gates

1. Docker image builds.
2. Container starts.
3. Required dependencies are reachable.
4. Healthcheck behaves as expected.
5. Configuration is injectable without rebuilding the image.
6. Container exits cleanly when expected.

## Avoid

- shipping development-only services
- unnecessary sidecars
- embedding secrets
- relying on host-specific paths
- adding containers merely to appear production-like
