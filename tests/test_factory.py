from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from harnessctl.core.factory import generate_harness
from harnessctl.core.validator import validate_dedicated


class FactoryTests(unittest.TestCase):
    def test_generates_dedicated_harness(self) -> None:
        profile = {
            "schema_version": "1",
            "identity": {
                "proposed_product_name": "Demo Service",
                "proposed_repository_name": "demo-service",
                "short_description": "demo",
                "problem_statement": "demo",
                "selected_architecture": "simple",
            },
            "domain": {
                "actors": [],
                "core_concepts": [],
                "entities": [],
                "business_rules": [],
            },
            "technical": {
                "application_type": "HTTP API",
                "persistence": "none",
                "interfaces": ["HTTP"],
                "external_dependencies": [],
            },
            "constraints": [],
            "risks": [],
            "open_questions": [],
        }

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            profile_path = root / "profile.json"
            output = root / "project"
            profile_path.write_text(json.dumps(profile), encoding="utf-8")

            result = generate_harness(profile_path, "0.1.0", output)

            self.assertTrue(result["valid"])
            validation = validate_dedicated(output)
            self.assertTrue(validation["valid"])


if __name__ == "__main__":
    unittest.main()
