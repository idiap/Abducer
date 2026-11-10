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


class LooperDependencyGraphTests(unittest.TestCase):
    def test_dependency_graph_contains_real_artifact_roles(self) -> None:
        result = subprocess.run(
            [sys.executable, "agentic/scripts/run_target_navigation.py", "--target",
             "agentic/examples/targets/p-vs-np-target.json"],
            cwd=ROOT, check=False, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
        graph = json.loads((ROOT / "agentic/state/dependency_graphs/p-vs-np.json").read_text(encoding="utf-8"))
        kinds = {node["kind"] for node in graph["nodes"]}
        self.assertIn("target", kinds)
        self.assertIn("pathway", kinds)
        self.assertIn("proof-sketch", kinds)
        # Existing proof-work nodes remain part of the dependency graph;
        # their presence does not authorize this uncommissioned CLI release.
        self.assertIn("proof_queue_entry", kinds)
        self.assertTrue(graph["frontier"], "real target should retain open mathematical dependency frontier")

    def test_dependency_graph_validator_rejects_dangling_edge(self) -> None:
        import tempfile

        graph = json.loads((ROOT / "agentic/state/dependency_graphs/p-vs-np.json").read_text(encoding="utf-8"))
        graph["edges"].append({"from": "missing", "to": graph["nodes"][0]["id"], "kind": "bad", "source_artifact": "test"})
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad-graph.json"
            bad.write_text(json.dumps(graph), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "agentic/scripts/validate_dependency_graph.py"), str(bad)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unknown source node", result.stderr)


if __name__ == "__main__":
    unittest.main()
