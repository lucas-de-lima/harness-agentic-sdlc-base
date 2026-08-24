# Changelog

## v0.31.0 — 2026-08-24

### Portability & Versioning

- First independently versioned Git release of the Base Harness.
- Repackaged as a standalone Git repository with semantic tag `v0.31.0`.
- Created `.gitignore` for Python, OS artifacts, and distribution artifacts.
- Removed generated Dedicated Harness artifact from `projects/blogs-api/.harness/`
  (project-specific generated content does not belong in the Base).
- Replaced absolute workspace path (`D:\Projetos\...`) with generic placeholders
  in `docs/GITHUB_IDENTITY_GUARDRAIL.md`.

### Validation

- All 127 tests pass.
- `make validate` (validate_base_repo.py) reports VALID.
- No absolute paths, secrets, or workspace-specific credentials found in the
  distribution scope.
- Factory, Vault, GitHub identity, branching, HITL, merge, and all core capabilities
  are portable and function without the original workspace.
- Distribution ZIP (`agentic-sdlc-base-v0.31.0.zip`) excludes:
  - `projects/` (legacy product project specs — not Base Harness components)
  - `fases-01-31/` (old ZIP snapshots — superseded by Git versioning)
  - `__pycache__/`, `.git/`, runtime artifacts

### Capabilities preserved

All 7 canonical workflows, 6 canonical skills, Vault knowledge graph, HITL gate
enforcement, controlled merge path, GitHub identity preflight, branching validation,
gitignore generation, Harness Factory, and Dedicated Harness validation remain
fully operational.