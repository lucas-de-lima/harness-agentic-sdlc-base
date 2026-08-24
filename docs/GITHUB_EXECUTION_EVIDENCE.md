# GitHub Execution Evidence

## Purpose

Define the minimal evidence written back to the GitHub work item.

## Completion comment

A successful workflow should record:

- workflow ID
- execution ID
- agent
- result
- changed artifacts
- validation summary
- unresolved questions
- next recommended action

## Principle

The comment is an index into evidence, not a replacement for detailed artifacts.

Large outputs remain in the repository or execution ledger.

## No secret leakage

Comments must never contain:

- access tokens
- credentials
- private keys
- full secret environment variables
- sensitive local filesystem paths when unnecessary
