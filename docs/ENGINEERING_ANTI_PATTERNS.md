# Engineering Anti-Patterns

**Status:** v0.1
**Scope:** Harness Base and Dedicated Harnesses

These are warning signals, not absolute prohibitions. The burden is on the design to justify them.

## Architecture

- Clean Architecture by template rather than by need.
- Microservices without independent deployment or scaling requirements.
- Event-driven design without meaningful asynchronous/event semantics.
- Layers that only forward calls.
- Modules that do not have real boundaries.

## Go

- Interface-everything design.
- Generic abstractions with no repeated problem to solve.
- Goroutines without a clear lifetime and cancellation strategy.
- Channels used where a simple synchronous call would be clearer.
- Global mutable state.
- Reflection-heavy dependency injection for small services.
- Custom utility frameworks replacing straightforward standard-library code.

## Testing

- Tests that assert implementation details rather than behavior.
- Excessive mocking of internal details.
- End-to-end tests for every small unit of behavior.
- Coverage targets that encourage meaningless tests.

## Dependencies

- Libraries introduced because they are fashionable.
- Multiple libraries solving the same small concern.
- Heavy frameworks for simple APIs.

## Operations

- Production-grade infrastructure for a portfolio project without an operational requirement.
- Distributed observability stacks for systems too small to need them.
- Complex deployment machinery that provides no meaningful learning or system value.

## Agent Behavior

- Making large speculative refactors before understanding the current system.
- Changing architecture without an accepted decision.
- Treating every task as permission to improve unrelated code.
- Hiding failures by weakening tests or checks.
- Continuing to add sophistication after the acceptance criteria are already satisfied.
