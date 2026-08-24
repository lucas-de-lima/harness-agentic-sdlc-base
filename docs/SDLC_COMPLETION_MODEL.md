# SDLC Completion Model

## Purpose

Separate work completion from system readiness and release readiness.

## States

```text
Task Done
   ↓
Feature Complete
   ↓
Epic Complete
   ↓
System Release Candidate
   ↓
Released
```

## Task Done

A single work item passed Code Review.

## Feature Complete

All required Stories and Tasks for the Feature are Done and feature-level validation passes.

## Epic Complete

All required Features are complete and epic-level acceptance is satisfied.

## Release Candidate

The product passes project release gates:

- build
- tests
- integration checks
- security checks
- documentation
- Docker/runtime validation
- CI success
- release metadata where applicable

## Released

The project has a reproducible release artifact and release evidence.

## Principle

A green Task does not imply a green system.
