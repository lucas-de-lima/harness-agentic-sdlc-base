---
name: project-discovery
description: Analyze a legacy project specification and repository to produce an evidence-backed Project Profile, proposed product/repository naming, domain understanding, technical characteristics, risks, and unresolved questions. Use when starting discovery of a legacy project before architecture selection or implementation planning.
---

# Project Discovery

This is the Codex runtime projection of the Base Harness `project-discovery` skill.

Follow the canonical procedure in the Base Harness documentation. The skill is intentionally read-only with respect to production code.

## Runtime entrypoint

Use the current repository as the project boundary. Resolve the repository root before inspecting files.

## Output

Produce the Project Profile requested by the active workflow. Do not implement code or choose architecture.
