# harnessctl Commands

## Validate Base

```bash
python -m harnessctl.cli validate . --kind base
```

## Generate Dedicated Harness

```bash
python -m harnessctl.cli generate \
  --profile examples/project-profile.json \
  --base-version 0.1.0 \
  --output /tmp/example-dedicated-harness
```

## Validate Dedicated Harness

```bash
python -m harnessctl.cli validate /tmp/example-dedicated-harness --kind dedicated
```

## Docker

```bash
docker build -t agentic-sdlc-base .
docker run --rm -v "$PWD:/workspace" agentic-sdlc-base validate /workspace --kind base
```

The implementation is deterministic and does not call an LLM.
