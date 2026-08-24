# GitHub Identity Guardrail

## Purpose

Prevent incorrect GitHub repository identity from causing operations against the wrong
repository. This guardrail was introduced after a real incident where an agent inferred
`owner/repository` from the local folder path and attempted GitHub operations against the
wrong account.

## Root cause

The local directory name and its parent path are **not** trusted sources of GitHub
identity. A project cloned into a local folder named `projects/my-project` does not
mean the GitHub repository is `my-org/my-project` or `projects/my-project` or any
path-derived name. The folder could be a fork, a renamed clone, a local working copy, or a
misleadingly-named directory.

## Rule

> Never infer GitHub `owner/repository` from the local path or folder name.

Before any GitHub operation (issue, PR, project field, comment, label, status transition),
the agent must resolve the repository identity from trusted sources and validate
consistency.

## Trusted sources (in authority order)

1. **Git repository root** — the `.git` directory confirms the working tree is a real repo.
2. **`origin` remote** — the configured remote URL is the primary identity source. It is
   the source of truth for where this clone came from.
3. **GitHub authenticated identity** — the user/login authenticated via `gh` or the GitHub
   MCP server. This confirms who is performing the operation, not which repo.
4. **Dedicated Harness explicit identity** — `confirmed_github_identity` in
   `.harness/manifest.json`, recorded after the first successful preflight. This is a
   cache of a previously-validated identity, not a substitute for validation.

## Resolution procedure

```
1. Find the Git repository root (walk up to .git).
2. Read git remotes; extract the `origin` remote.
3. Parse the GitHub owner/repository from the origin URL.
4. If a confirmed_github_identity exists in .harness/manifest.json, cross-check it.
5. If an explicit owner/repo is provided, cross-check it.
6. If all sources agree → proceed. Record the identity if not yet recorded.
7. If any source disagrees → HALT. Report the divergence. Do not guess.
8. If no origin remote exists → HALT. Report the missing remote. Do not guess.
```

## Failure modes (all halt)

| Condition | Behavior |
|---|---|
| No `.git` directory | Halt: "Not inside a Git repository." |
| No `origin` remote | Halt: "No GitHub 'origin' remote found. Cannot infer from local path." |
| `origin` is not a GitHub URL | Halt: the remote is not a GitHub repository. |
| `origin` owner/repo differs from harness identity | Halt: "identity divergence." Report both. |
| `origin` owner/repo differs from explicit expected | Halt: "identity divergence." Report both. |
| Local path name is misleading (e.g., `my-workspace/projects/my-project`) | Does not matter — path is never used as identity. |

## Tooling

### `harnessctl preflight`

```sh
harnessctl preflight --path <project-dir> [--owner <login>] [--repo <name>] [--record]
```

Returns JSON with `ok`, `canonical_owner`, `canonical_repo`, `origin`, `errors`, and
`warnings`. Exit code 0 on success, 1 on failure.

Use `--record` to write the confirmed identity into `.harness/manifest.json` after the
first successful validation. Subsequent operations can then cross-check against the
recorded identity.

### `harnessctl gitignore`

```sh
harnessctl gitignore <project-dir> --language go
harnessctl gitignore <project-dir> --language go --check
```

Generates or validates a stack-appropriate `.gitignore` before the first commit/push.
Supported languages: `go`, `node`, `python`, `generic`. `--check` validates only.

## Project bootstrap requirement

Before the first commit or push in a product repository:

1. Run `harnessctl preflight --record` to confirm and register the canonical identity.
2. Run `harnessctl gitignore --language <stack>` to generate the `.gitignore`.
3. Only after both pass may the bootstrap proceed to commit/push.

This prevents accidentally committing secrets, build artifacts, or environment files, and
ensures the repository identity is known and verified before any GitHub state is created.

## Scope

This guardrail is generic. It applies to all Dedicated Harnesses and all product
repositories. No rule in this document is specific to `editorial-hub-api` or any other
single project.

## Relationship to existing GitHub capabilities

This guardrail does **not** remove or disable any working GitHub capability. It adds a
preflight validation step that must run before GitHub operations. If the preflight passes,
all existing capabilities (issue creation, project field updates, status transitions,
sub-issue linking) work exactly as before. If the preflight fails, the operation must not
proceed until the divergence is resolved by a human.
