from __future__ import annotations
import json, sys
from pathlib import Path

REQUIRED = ["schema_version","identity","domain","technical","constraints","risks","open_questions"]
IDENTITY = ["proposed_product_name","proposed_repository_name","problem_statement","short_description"]
DOMAIN = ["actors","core_concepts","entities","business_rules"]
TECHNICAL = ["application_type","persistence","interfaces","external_dependencies"]

def fail(msg: str) -> None:
    print(f"INVALID: {msg}")
    raise SystemExit(1)

def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_discovery.py <profile.json>")
        return 2
    p = Path(sys.argv[1])
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot read JSON: {exc}")

    if not isinstance(data, dict):
        fail("profile must be an object")

    for k in REQUIRED:
        if k not in data:
            fail(f"missing top-level key: {k}")

    for k in IDENTITY:
        if k not in data["identity"]:
            fail(f"missing identity key: {k}")

    for k in DOMAIN:
        if k not in data["domain"]:
            fail(f"missing domain key: {k}")

    for k in TECHNICAL:
        if k not in data["technical"]:
            fail(f"missing technical key: {k}")

    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
