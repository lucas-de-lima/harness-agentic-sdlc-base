# ADR-001: Select a Simple HTTP API Architecture

## Status

Proposed

## Context

The system is a small HTTP API with a limited domain, one persistence system, and no meaningful requirement for independent service deployment.

## Decision

Select the `simple` architecture profile with clear internal separation where those boundaries provide real value.

## Simplest Viable Architecture

A single Go process with a small internal structure is sufficient.

## Alternatives Considered

### Layered

Useful if separation needs to become more pronounced, but adds structure that is not currently necessary.

### Hexagonal

Useful when multiple interchangeable adapters are a real requirement, but current evidence does not establish that.

## Rejected Alternatives

Hexagonal is rejected for now because the project has a small integration surface and no immediate need for multiple interchangeable adapters.

## Consequences

### Positive

- low cognitive overhead
- easy local execution
- straightforward testing
- low operational burden

### Negative

- stronger separation may need to be introduced later if integrations grow

## Future Evolution Triggers

- multiple external implementations become first-class
- domain complexity materially increases
- independently deployable boundaries become justified
