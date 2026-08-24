# Release Candidate Workflow

## Trigger

Epic or project enters `Release Candidate`.

## Steps

1. Freeze release scope.
2. Run build.
3. Run unit tests.
4. Run integration tests.
5. Run security/quality checks.
6. Build Docker artifact when applicable.
7. Run container/runtime checks.
8. Validate documentation.
9. Validate CI.
10. Generate Release Report.
11. Resolve findings.
12. Approve release candidate.

## Outcomes

- `Release Ready`
- `Release Blocked`

## No automatic production deployment

This Base Harness does not assume production deployment.

Deployment is project-specific and may be added later.
