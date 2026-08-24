# Go Engineer E2E Task Selection

## Choose the first pilot Task

Prefer a Task that:

- changes a single cohesive behavior
- has explicit acceptance criteria
- has a small test surface
- does not require external credentials
- does not require database migration unless already trivial
- does not require a new infrastructure component
- does not require architecture changes

## Good first examples

- health endpoint
- simple domain validation
- one CRUD operation
- one HTTP handler backed by existing application structure
- one small persistence operation

## Avoid for first execution

- authentication
- distributed workflows
- migrations with production data
- broad refactors
- concurrency-heavy features
- multiple external integrations
