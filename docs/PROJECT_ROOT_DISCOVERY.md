# Project Root Discovery

## Purpose

Define how agents determine what repository/layer they are operating in.

## Discovery order

1. Identify the Git repository root.
2. Search upward from the current working directory for the nearest `.harness/`.
3. Inspect repository-level agent instruction files recognized by the active agent runtime.
4. Load `.harness/project-profile.md` when present.
5. Load `.harness/README.md` and applicable project policies.
6. Resolve the current task from GitHub when the task originated there.
7. Only then select project skills and workflows.

## Root categories

### Base Harness root

Indicators:

- Base Constitution
- Base catalogs
- Base Factory
- no product-specific `.harness/project-profile.md`

### Dedicated Harness / product root

Indicators:

- `.harness/`
- project profile
- project architecture decision
- Go application

### Subdirectory

If execution begins inside a subdirectory, agents must resolve the repository root before deciding what instructions apply.

## Safety rule

Never assume the current directory is the system boundary.

Repository root detection is mandatory before destructive or architectural changes.
