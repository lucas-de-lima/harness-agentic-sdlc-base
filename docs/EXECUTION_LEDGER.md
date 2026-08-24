# Execution Ledger

## Purpose

Provide an append-only record of agent workflow execution.

## Minimum fields

- execution_id
- workflow_id
- work_item_id
- repository
- agent
- started_at
- completed_at
- status
- attempt
- inputs
- outputs
- validations
- errors
- next_action

## Principle

The ledger records what happened. It does not become a second task-management system.

Operational work state remains in GitHub when the project is connected to GitHub Projects.
