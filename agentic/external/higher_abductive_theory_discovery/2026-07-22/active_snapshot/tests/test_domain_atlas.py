import unittest

from tdr.atlas import map_fragment, propose_morphism
from tdr.domain.models import EvidenceRef, canonical_json, stable_id


class DomainAtlasTests(unittest.TestCase):
    def test_stable_id_is_presentation_order_invariant_for_dicts(self):
        self.assertEqual(stable_id("x", {"a": 1, "b": 2}), stable_id("x", {"b": 2, "a": 1}))

    def test_evidence_bounds_are_checked(self):
        with self.assertRaises(ValueError):
            EvidenceRef("a", "L1", "paper", 1.1)

    def test_fragment_retains_source_and_scope(self):
        fragment = map_fragment({
            "name": "Groups",
            "sources": [{"artifact_id": "paper", "locator": "sec2", "content": "Sort: G\nSymbol: mul : G x G -> G\nAxiom: associativity\nClaim: identity is unique\nScope: ordinary groups"}],
        })
        self.assertEqual(fragment.regime["statements"], ["ordinary groups"])
        self.assertEqual(fragment.claims[0]["source_ref"]["locator"], "sec2:L4")
        self.assertEqual(fragment.lifecycle, "staged")

    def test_morphism_reports_missing_symbols_and_scope(self):
        morphism = propose_morphism({
            "source_fragment": {"fragment_id": "a", "symbols": {"mul": "GxG->G", "unit": "G"}, "axioms": ["assoc"], "regime": {"r": 1}},
            "target_fragment": {"fragment_id": "b", "symbols": {"times": "HxH->H"}},
            "symbol_map": {"mul": "times"},
        })
        self.assertFalse(morphism.total_on_declared_domain)
        self.assertTrue(any("unit" in item for item in morphism.obligations))
        self.assertTrue(any("scope" in item for item in morphism.obligations))

    def test_canonical_json_is_deterministic(self):
        self.assertEqual(canonical_json({"z": [2, 1], "a": True}), '{"a":true,"z":[2,1]}')


if __name__ == "__main__":
    unittest.main()

