# E2E Validation Checklist

## Before execution

- [ ] GitHub MCP is connected.
- [ ] Read-only tool inventory is known.
- [ ] The selected product repository is correct.
- [ ] Project exists.
- [ ] `DISCOVERY-001` exists.
- [ ] `DISCOVERY-001` is `Ready`.
- [ ] Inherited project specification exists.
- [ ] Dedicated Harness, if any, is discoverable.

## During execution

- [ ] Agent reads Issue before acting.
- [ ] Agent reads repository context.
- [ ] Agent uses `project-discovery`.
- [ ] Agent does not modify production code.
- [ ] Agent records evidence.
- [ ] Project Profile validates.

## After execution

- [ ] Handoff Packet exists.
- [ ] Execution evidence was recorded.
- [ ] Exactly one bounded GitHub comment was added.
- [ ] Issue status is `In Review`.
- [ ] No unrelated Issues/Projects were modified.
- [ ] Git diff contains only expected discovery artifacts.
