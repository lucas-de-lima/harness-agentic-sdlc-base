# Bootstrap Commands

## Inspect a real project without writing

```bash
python scripts/bootstrap_dedicated_harness.py \
  --project /path/to/project \
  --profile /path/to/project-profile.json \
  --base-version 0.29.0 \
  --check-only
```

## Generate

```bash
python scripts/bootstrap_dedicated_harness.py \
  --project /path/to/project \
  --profile /path/to/project-profile.json \
  --base-version 0.29.0 \
  --harness-version 0.1.0
```

## Validate

```bash
python scripts/validate_dedicated_harness.py /path/to/project
```

## Audit diff

```bash
python scripts/audit_bootstrap_diff.py /path/to/project
```

## Important

These commands do not commit or push.
