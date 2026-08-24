# Repository Architecture

## Purpose

Define the physical boundaries between the Base Harness, Dedicated Harness, application code, and operational infrastructure.

## Base Harness repository

The Base Harness is an independent repository.

Conceptual structure:

```text
agentic-sdlc-base/
├── README.md
├── docs/
├── skills/
├── agents/
├── templates/
├── policies/
├── workflows/
├── tools/
└── scripts/
```

The Base Harness contains reusable capabilities and governance.

## Product repository

Each system has its own repository.

Conceptual structure:

```text
project-x/
├── .harness/
├── .github/
├── cmd/
├── internal/
├── pkg/              # only when a real public/reusable package exists
├── tests/
├── docs/
├── scripts/
├── Dockerfile
├── compose.yaml
├── go.mod
├── go.sum
├── Makefile
└── README.md
```

The exact Go layout is decided by the project's architecture, not by this template.

## Boundary

```text
Base Harness
    └── creates/specializes
        Dedicated Harness
            └── governs
                Product System
```

The Dedicated Harness is versioned in the product repository.

## `.harness`

The `.harness` directory contains project-specific agentic engineering configuration and context.

It must not become a second source of product requirements or a duplicate backlog.
