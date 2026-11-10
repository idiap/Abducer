import unittest

from tdr.validation import falsify, formalize, instantiate, prove_transport


CANDIDATE = {
    "candidate_id": "c1",
    "formal_move": "Adjoin witness W(A)",
    "atlas_patch": {"objects": ["A"], "morphisms": ["u"]},
    "assumptions": ["scope is preserved"],
    "return_paths": [{"target": "finite model", "method": "enumerate"}],
    "consequences": ["held-out theorem"],
}


class ValidationTests(unittest.TestCase):
    def test_formalization_emits_exact_obligations_and_skeletons(self):
        outcome = formalize({"candidate": CANDIDATE})
        self.assertEqual(outcome.status, "partial")
        self.assertTrue(any("discharge assumption" in item for item in outcome.obligations_remaining))
        self.assertTrue(any("theorem" in item for item in outcome.evidence_artifacts))

    def test_unbalanced_formal_move_blocks(self):
        candidate = {**CANDIDATE, "formal_move": "F(A"}
        self.assertEqual(formalize({"candidate": candidate}).status, "blocked")

    def test_transport_excludes_trivial_restatement(self):
        outcome = prove_transport({
            "morphism": {"morphism_id": "m", "total_on_declared_domain": True, "scope_map": {"A": "B"}, "obligations": []},
            "theorems": [{"name": "t", "statement": "A -> A", "target_statement": "A -> A"}],
        })
        self.assertTrue(any("trivial" in item for item in outcome.findings))

    def test_instantiation_keeps_error_obligation(self):
        outcome = instantiate({"candidate": CANDIDATE, "targets": ["finite model"]})
        self.assertTrue(any("error" in item for item in outcome.obligations_remaining))

    def test_adversarial_failure_is_retained(self):
        outcome = falsify({"candidate": CANDIDATE, "test_results": {"degenerate_case": "falsified"}})
        self.assertEqual(outcome.status, "falsified")
        self.assertIn("degenerate_case", outcome.falsifying_conditions)


if __name__ == "__main__":
    unittest.main()

