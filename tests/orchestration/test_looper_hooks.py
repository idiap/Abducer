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

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def _run_hook(script: str, payload: dict) -> dict:
    result = subprocess.run(
        [sys.executable, script],
        cwd=ROOT,
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout.strip().splitlines()[-1])


class LooperHookTests(unittest.TestCase):
    def test_hook_contract_fixtures_pass(self) -> None:
        result = subprocess.run(
            [sys.executable, "agentic/scripts/run_hook_contract_tests.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("validated 5 hook contract fixtures", result.stdout)

    def test_pre_skill_hook_blocks_undeclared_controlled_skill(self) -> None:
        payload = _run_hook("hooks/scripts/pre_skill_use_policy.py", {"skill": "not-declared", "controlled": True})
        self.assertEqual(payload["decision"], "block")

    def test_pre_tool_hook_blocks_destructive_command(self) -> None:
        payload = _run_hook("hooks/scripts/pre_tool_use_policy.py", {"command": "rm -rf /tmp/example"})
        self.assertEqual(payload["decision"], "block")


if __name__ == "__main__":
    unittest.main()
