# Agentic SDLC Base

## Status

Phase 31 — Real Project Discovery: ready for execution.

This phase is the first one that operates on one of the user's actual seven project repositories.

## Read-only discovery

```bash
python scripts/inspect_real_project.py   --project /path/to/project   --output /tmp/project-discovery
```

Then create/review the Project Profile and evidence before generating the Dedicated Harness.

No production files should be modified by discovery.
