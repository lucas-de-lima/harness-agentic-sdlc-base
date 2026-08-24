# Workflow Guardrails

## Mandatory

- bounded execution
- explicit state
- explicit authority
- evidence after mutation
- validation before completion
- review independence where required
- **human-in-the-loop gates** (see `HITL_POLICY.md`) — merges, releases, architecture
  changes, scope changes, destructive actions, and security exceptions require explicit
  human approval. The workflow must PAUSE when a Human Gate is pending.

## Forbidden

- infinite agent loops
- silent retries
- silent scope expansion
- declaring Done from code generation alone
- changing architecture without architectural authorization
- bypassing failed quality gates
- closing work items without evidence
- **automating a merge** (story→feature, feature→develop, develop→main) without a Human Gate
- **bypassing `harnessctl merge`** — every merge must go through `harnessctl merge`,
  which enforces the HITL gate check. Calling `github_merge_pull_request` or `gh pr merge`
  directly is a policy violation.
- **auto-approving** via timeout, silence, or polling
- **transforming a blocked decision into an approved one** by inference

## Emergency stop conditions

Stop immediately on:

- security-critical unexpected behavior
- destructive action outside authorization
- detected prompt/instruction conflict affecting safety
- repository boundary uncertainty
- inconsistent workflow state
