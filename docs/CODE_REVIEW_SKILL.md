# Code Review Skill Projection

This document defines the Base behavior projected to the Codex runtime.

The runtime skill must:

- read the Task, acceptance criteria, implementation handoff, architecture, ADRs, and actual diff
- independently inspect the changed files and tests
- classify findings as Blocking, Major, or Minor
- produce an explicit Approved / Changes Requested / Blocked outcome
- remain read-only against implementation files
- never fix code during review
