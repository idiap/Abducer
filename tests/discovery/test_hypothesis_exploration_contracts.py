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
import shutil
import subprocess
import sys
import unittest
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class HypothesisExplorationContractTests(unittest.TestCase):
    """Check P-vs-NP artifacts from an uncommissioned run that must stay on hold."""

    @classmethod
    def setUpClass(cls) -> None:
        # This CLI writes shared graphs, fixtures, logs and documentation. Save
        # tracked outputs before invocation and register cleanup before setup can
        # fail, so later tests see the original scientific state and SD headers.
        tracked = (
            subprocess.run(
                ["git", "ls-files", "-z"], cwd=ROOT, check=True, capture_output=True
            )
            .stdout.decode()
            .split("\0")
        )
        prefixes = (
            "agentic/state/",
            "agentic/traces/",
            "agentic/logs/",
            "agentic/fixtures/hegelian/",
            "artifacts/hegelian/",
            "tests/fixtures/hegelian/",
            "tests/generative/fixtures/",
        )
        documents = {
            "docs/integrations/hegelian-source-map.md",
            "docs/research-methods/conceptual-creativity-operations.md",
        }
        originals = {
            ROOT / name: (ROOT / name).read_bytes()
            for name in tracked
            if name
            and (
                name.startswith(prefixes)
                or name in documents
                or (name.startswith("agentic/reports/") and name.endswith(".md"))
            )
            and (ROOT / name).is_file()
            and not (ROOT / name).is_symlink()
        }
        run_id = f"sd-test-navigation-{uuid.uuid4().hex}"

        def restore_outputs() -> None:
            for path, original in originals.items():
                if not path.exists() or path.read_bytes() != original:
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_bytes(original)
            # Remove only this invocation's uniquely named generated run files.
            for directory in ("reports", "traces", "logs"):
                matches = (ROOT / "agentic" / directory).rglob(f"*{run_id}*")
                for path in sorted(matches, key=lambda p: len(p.parts), reverse=True):
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink(missing_ok=True)

        cls.addClassCleanup(restore_outputs)
        result = subprocess.run(
            [
                sys.executable,
                "agentic/scripts/run_target_navigation.py",
                "--run-id",
                run_id,
                "--target",
                "agentic/examples/targets/p-vs-np-target.json",
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        # No canonical theory evidence is supplied: artifact generation is
        # valid, but the CLI must keep release authority blocked (exit 3).
        assert result.returncode == 3, result.stdout + result.stderr
        for path, original in originals.items():
            if path.is_relative_to(ROOT / "tests"):
                assert path.read_bytes() == original, f"runtime rewrote fixture: {path}"
        receipt_path = (
            ROOT
            / "agentic/reports/releases/targets/p-vs-np-target/runs"
            / run_id
            / "release.json"
        )
        assert (
            json.loads(receipt_path.read_text(encoding="utf-8"))["decision"] == "hold"
        )

    def test_hypothesis_map_validates_and_has_route_diversity(self) -> None:
        result = subprocess.run(
            [sys.executable, "agentic/scripts/validate_hypothesis_exploration.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(
            (ROOT / "artifacts/hegelian/hypothesis_exploration_map.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertGreaterEqual(payload["summary"]["candidate_count"], 8)
        self.assertGreaterEqual(len(payload["summary"]["creative_operations"]), 4)
        self.assertNotIn("proof_queue", payload["summary"]["dispositions"])
        self.assertNotIn("discovery_branch", payload["summary"]["dispositions"])
        self.assertIn("evidence_task", payload["summary"]["dispositions"])
        self.assertIn("revision_loop", payload["summary"]["dispositions"])

    def test_generated_artifact_family_is_complete(self) -> None:
        required = [
            "artifacts/hegelian/hypothesis_exploration_map.json",
            "artifacts/hegelian/failure_signal_cartography.json",
            "artifacts/hegelian/mediation_candidates.json",
            "artifacts/hegelian/validation_packets.json",
            "artifacts/hegelian/candidate_rankings.json",
            "artifacts/hegelian/conceptual_refinement_trace.json",
            "agentic/logs/hegelian-conceptual-refinement.jsonl",
            "agentic/reports/hegelian_conceptual_refinement_release_report.md",
            "agentic/reports/hegelian_abducer_coherence_review.md",
            "docs/integrations/hegelian-source-map.md",
            "docs/research-methods/conceptual-creativity-operations.md",
        ]
        for raw in required:
            self.assertTrue((ROOT / raw).exists(), raw)

    def test_dependency_graph_exposes_creative_nodes(self) -> None:
        graph = json.loads(
            (ROOT / "agentic/state/dependency_graphs/p-vs-np.json").read_text(
                encoding="utf-8"
            )
        )
        kinds = {node["kind"] for node in graph["nodes"]}
        self.assertIn("conceptual_pressure", kinds)
        self.assertIn("creative_candidate", kinds)
        self.assertIn("validation_obligation", kinds)
        edges = {edge["kind"] for edge in graph["edges"]}
        self.assertIn("motivates-creative-candidate", edges)
        self.assertIn("has-validation-obligation", edges)


if __name__ == "__main__":
    unittest.main()
