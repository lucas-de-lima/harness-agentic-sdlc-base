---
name: project-discovery
description: Analyze a legacy project specification and repository to produce an evidence-backed Project Profile, proposed product/repository naming, domain understanding, technical characteristics, risks, and unresolved questions. Use when starting discovery of a legacy project before architecture selection or implementation planning.
---

# Project Discovery

## Purpose

Transform an ambiguous legacy project into a structured Project Profile.

## Operating mode

Read-only with respect to production code.

Do not modify application source, dependencies, Docker configuration, CI, or architecture.

## Inputs

Use the materials available in the current repository:

1. the inherited project `.md` specification
2. repository structure
3. legacy source code when present
4. existing configuration
5. tests and fixtures when present

Inspect before concluding.

## Naming rules

Propose:

- product name
- repository name

Ignore inherited school-specific names or branding when they are historical rather than functional requirements.

Do not preserve a legacy name merely because it appears in a filename.

## Discovery procedure

1. Locate the project repository root.
2. Identify the primary inherited specification.
3. Inspect the specification completely.
4. Inspect the repository structure.
5. Inspect relevant source files, configuration, tests, and data examples.
6. Extract actors, domain concepts, entities, workflows, and business rules.
7. Extract technical characteristics:
   - application type
   - interfaces
   - persistence
   - integrations
   - concurrency
   - operational concerns
8. Separate explicit requirements from inferred behavior.
9. Record risks and ambiguities.
10. Produce the Project Profile.

## Evidence discipline

For every important inferred rule, identify the evidence source.

Prefer:

- specification text
- tests
- observable code behavior
- configuration

over assumptions.

When evidence conflicts, report the conflict instead of silently choosing one interpretation.

## Required output

Write the Project Profile to the location specified by the surrounding workflow.

It must include:

- identity
- problem statement
- short description
- actors
- core concepts
- entities
- business rules
- application type
- persistence
- interfaces
- external dependencies
- constraints
- risks
- open questions
- evidence references

## Boundary

Do not choose final architecture.

Do not create GitHub work items.

Do not implement features.

Do not decide technology merely because it is familiar.

## Verification

Before finishing:

- confirm the profile contains all required sections
- confirm open questions are explicit
- confirm naming is independent of historical school branding
- confirm no production files were modified
