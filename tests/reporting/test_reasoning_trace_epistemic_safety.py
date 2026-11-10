#!/usr/bin/env python3
# SPDX-FileCopyrightText: © 2026 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Andre Freitas <andre.freitas@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
# Neuro-symbolic AI Group
#
# SPDX-License-Identifier: MIT
"""Adversarial semantic checks for the workflow-neutral trace."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "agentic/scripts/validate_public_reasoning_trace.py"
sys.path.insert(0, str(SCRIPT.parent))
SPEC = importlib.util.spec_from_file_location("public_trace_validator", SCRIPT)
VALIDATOR = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)


def event(event_id: str, sequence: int, **updates):
    value = {
        "event_id": event_id,
        "sequence": sequence,
        "event_family": "public_inference",
        "causal_parent_event_ids": [],
        "public_inference": {
            "question": "Is the bounded claim supported?",
            "premises": [{"type": "artifact", "statement": "A finite certificate is present."}],
            "warrant": "The certificate checks the declared finite instance.",
            "conclusion": "The finite claim is supported."
        },
        "evidence": [{"relation": "supports", "path": "artifacts/certificate.json", "artifact_type": "Certificate"}],
        "claim_epistemic_status": "evidence_backed",
        "authority": {"exercised": ["finite-check"], "absent": ["continuum-promotion"], "prohibitions_checked": []},
    }
    value.update(updates)
    return value


class ReasoningTraceEpistemicSafetyTests(unittest.TestCase):
    def _codes(self, events):
        trace = {"run_id": "run.safety", "workflow_id": "theorem_proof_delivery", "events": events}
        return {issue.code for issue in VALIDATOR.validate_trace(trace)}

    def test_valid_bounded_public_rationale_passes(self) -> None:
        self.assertEqual(self._codes([event("e1", 1)]), set())

    def test_invalid_parent_and_cycle_are_rejected(self) -> None:
        missing = event("e1", 1, causal_parent_event_ids=["absent"])
        self.assertIn("missing-causal-parent", self._codes([missing]))
        first = event("e1", 1, causal_parent_event_ids=["e2"])
        second = event("e2", 2, causal_parent_event_ids=["e1"])
        self.assertIn("causal-cycle", self._codes([first, second]))

    def test_missing_rationale_and_invalid_evidence_relation_are_rejected(self) -> None:
        bad = event("e1", 1, public_inference={"conclusion": "Promote."}, evidence=[{"relation": "proves"}])
        codes = self._codes([bad])
        self.assertIn("missing-public-rationale", codes)
        self.assertIn("invalid-evidence-relation", codes)

    def test_absolute_artifact_path_is_rejected(self) -> None:
        bad = event("e1", 1, evidence=[{"relation": "supports", "path": "/tmp/private.json", "artifact_type": "Evidence"}])
        self.assertIn("non-portable-path", self._codes([bad]))

    def test_scope_widening_requires_evidence(self) -> None:
        bad = event("e1", 1, scope_transition={"before": "finite", "after": "continuum", "widens": True})
        self.assertIn("unsupported-scope-widening", self._codes([bad]))

    def test_blind_adjudication_identity_leak_is_rejected(self) -> None:
        bad = event("e1", 1, step_id="blind_adjudicate", candidate_owner="agent-A")
        self.assertIn("blind-identity-leak", self._codes([bad]))

    def test_unexplained_skip_is_rejected(self) -> None:
        bad = event("e1", 1, event_family="skip", public_inference={})
        self.assertIn("unexplained-skip", self._codes([bad]))

    def test_review_cannot_claim_proof_acceptance_authority(self) -> None:
        bad = event("e1", 1, workflow_id="deep_review_and_reorientation", authority={"exercised": ["proof_acceptance"], "absent": [], "prohibitions_checked": []})
        self.assertIn("review-authority-escalation", self._codes([bad]))

    def test_malformed_digest_is_rejected(self) -> None:
        bad = event("e1", 1, evidence=[{"relation": "supports", "path": "artifacts/evidence.json", "artifact_type": "Evidence", "digest": "forged"}])
        self.assertIn("malformed-evidence-digest", self._codes([bad]))

    def test_well_formed_but_forged_digest_is_rejected(self) -> None:
        bad = event(
            "e1", 1,
            evidence=[{
                "relation": "supports",
                "path": "tests/fixtures/reasoning_trace/evidence/workflow-evidence.json",
                "artifact_type": "Evidence",
                "digest": "0" * 64,
                "external": False,
            }],
        )
        self.assertIn("evidence-digest-mismatch", self._codes([bad]))

    def test_forged_or_mismatched_receipt_binding_is_rejected(self) -> None:
        unbound = event(
            "e1", 1,
            evidence=[{
                "relation": "supports", "path": "artifacts/evidence.json",
                "artifact_type": "Evidence", "receipt_id": "receipt-forged",
            }],
        )
        self.assertIn("unbound-evidence-receipt", self._codes([unbound]))

        mismatched = event(
            "e1", 1,
            evidence=[{
                "relation": "supports", "path": "artifacts/other.json",
                "artifact_type": "Evidence", "receipt_id": "receipt-1",
            }],
            receipts=[{"receipt_id": "receipt-1", "path": "artifacts/evidence.json"}],
        )
        self.assertIn("receipt-binding-mismatch", self._codes([mismatched]))

    def test_novelty_cannot_be_inflated_without_assessment_authority(self) -> None:
        bad = event(
            "e1", 1,
            public_inference={
                "question": "Is the result novel?",
                "premises": [{"type": "artifact", "statement": "One comparison exists."}],
                "warrant": "A partial comparison was made.",
                "conclusion": "The contribution is novel.",
            },
            claim_epistemic_status="validated",
            authority={"exercised": ["workflow-step"], "absent": ["novelty-assessment"], "prohibitions_checked": []},
        )
        self.assertIn("novelty-inflation", self._codes([bad]))

    def test_no_argument_release_gate_validates_all_named_workflow_fixtures(self) -> None:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--quiet"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
