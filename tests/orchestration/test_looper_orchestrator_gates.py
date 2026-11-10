# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class LooperOrchestratorGateTests(unittest.TestCase):
    def test_agentic_check_passes_end_to_end(self) -> None:
        result = subprocess.run(
            [sys.executable, "agentic/scripts/agentic_check.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("All Abducer Looper checks passed.", result.stdout)

    def test_agentic_check_default_contains_no_generators_or_navigation(self) -> None:
        result = subprocess.run(
            [sys.executable, "agentic/scripts/agentic_check.py", "--list"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        selected = result.stdout.splitlines()
        self.assertTrue(selected)
        self.assertTrue(
            all(Path(script).name.startswith("validate_") or Path(script).name == "run_hook_contract_tests.py" for script in selected)
        )
        self.assertNotIn("agentic/scripts/run_target_navigation.py", selected)
        self.assertEqual(len(selected), len(set(selected)))

    def test_workflow_contracts_and_promotion_gates_validate(self) -> None:
        for script in [
            "agentic/scripts/validate_workflow_contracts.py",
            "agentic/scripts/validate_promotion_gates.py",
        ]:
            result = subprocess.run([sys.executable, script], cwd=ROOT, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
