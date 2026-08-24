# Project Automation Policy

## Principle

Automate only transitions that are deterministic and safe.

## Allowed early automation

- automatic status synchronization where the source is unambiguous
- adding issues to the Project
- applying standard fields
- adding execution evidence

## Human/Orchestrator controlled

- moving a work item to Done
- overriding a blocked state
- closing high-impact issues
- architecture approval
- release readiness

## Why

GitHub Projects supports built-in workflows and automation, but the Agentic SDLC must not allow generic automation to bypass its own validation and authority model. citeturn197859search1

## Rule

Native GitHub automation and Agentic SDLC workflows should complement each other, not compete.

If both attempt to own the same state transition, the Agentic SDLC must define the authoritative transition.
