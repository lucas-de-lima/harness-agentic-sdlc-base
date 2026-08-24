from pathlib import Path
import argparse
import json

TEMPLATE = """# Project Profile — Real Project

## Identity

- Proposed product name:
- Proposed repository name:
- Problem statement:
- Short description:

## Domain

### Actors

### Core concepts

### Entities

### Business rules

### Primary workflows

## Technical

- Application type:
- Interfaces:
- Persistence:
- External dependencies:
- Concurrency characteristics:
- Runtime assumptions:

## Constraints

## Non-goals

## Risks

## Open questions

## Evidence
"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.output.exists():
        print("Refusing to overwrite existing profile:", args.output)
        return 1
    args.output.write_text(TEMPLATE, encoding="utf-8")
    print(args.output)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
