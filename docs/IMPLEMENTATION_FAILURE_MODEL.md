# Implementation Failure Model

## Correctable implementation defect

Fix within the current Task.

## Test failure

Investigate and fix when caused by the current change.

## Unclear requirement

Stop and escalate. Do not invent behavior.

## Architecture conflict

Stop and return to Architecture Deliberation.

## External dependency failure

Classify as Blocked when progress cannot continue without external intervention.

## Scope expansion

Stop and create/route follow-up work rather than silently expanding the current Task.

## Retry

Retries are bounded. Re-running a failed command is allowed when the failure is plausibly transient; redesigning blindly is not.
