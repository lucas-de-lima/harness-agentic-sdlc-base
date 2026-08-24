# Planning → Implementation Gate

## Conditions

Implementation may begin only when:

1. Architecture is Approved.
2. Planning is Ready.
3. The implementation Feature is `Ready` (default) or a Task is `Ready` (small work).
4. The Feature's User Stories have acceptance criteria.
5. Required dependencies are resolved (Feature-level and Task-level).
6. Relevant skills and tools are available.
7. The Go Engineer has authority for the Feature.
8. The `feature/<name>` branch can be created from `develop`.

## Prohibited

Planning itself must never move the implementation Feature or Task to `In Progress`.

The transition to `In Progress` belongs to the implementation workflow when a Go Engineer
claims the Feature or Task.
