import json
from pathlib import Path
import unittest

class ContractTest(unittest.TestCase):
    def test_contract_files_and_example(self):
        root = Path(__file__).parents[1]
        for relative in ("SKILL.md", "input.schema.json", "output.schema.json", "policy.yaml", "examples/minimal_input.json", "examples/expected_output.json"):
            self.assertTrue((root / relative).exists(), relative)
        output = json.loads((root / "examples/expected_output.json").read_text())
        self.assertIn(output["status"], ("completed", "partial", "blocked", "invalid"))
        self.assertEqual(set(("artifacts", "claims", "uncertainties", "next", "provenance")) - output.keys(), set())

if __name__ == "__main__":
    unittest.main()
