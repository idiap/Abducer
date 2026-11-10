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
import sys
import unittest
from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "agentic/scripts"))

from validate_task_skill_registry import taxonomy_ids, validate_manifest  # noqa: E402


class LooperWorkflowRegistryTests(unittest.TestCase):
    def test_task_skill_registry_validates(self) -> None:
        validate_manifest(ROOT / "registry/tasks/p-vs-np-target-navigation/task_registry.json", taxonomy_ids())

    def test_task_skill_registry_rejects_undeclared_skill(self) -> None:
        import tempfile

        manifest = json.loads((ROOT / "registry/tasks/p-vs-np-target-navigation/task_registry.json").read_text(encoding="utf-8"))
        manifest["visible_workflows"][0]["composed_skills"].append("not-declared")
        with tempfile.TemporaryDirectory() as tmp:
            task_dir = Path(tmp) / "bad-task"
            task_dir.mkdir()
            bad = task_dir / "task_registry.json"
            bad.write_text(json.dumps(manifest), encoding="utf-8")
            with redirect_stderr(StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    validate_manifest(bad, taxonomy_ids())
        self.assertEqual(raised.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
