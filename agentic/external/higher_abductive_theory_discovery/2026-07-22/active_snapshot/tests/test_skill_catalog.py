import unittest

from tdr.domain.schema import validate_skill_result
from tdr.skills import CATALOG, execute_skill


BASE_CANDIDATE = {
    "candidate_id": "c",
    "mode": "bridge",
    "formal_move": "add F : A -> B",
    "atlas_patch": {"objects": ["A", "B"], "morphisms": ["F"]},
    "assumptions": [],
    "consequences": ["recover theorem", "held-out consequence"],
    "falsifiers": ["no model"],
    "return_paths": [{"target": "model", "method": "construct"}],
    "validation_tasks": [{"type": "type_check"}],
    "pressure_ids": ["p"],
    "uncertainty": {},
}


class SkillCatalogTests(unittest.TestCase):
    def test_catalog_has_all_seventeen_skills(self):
        self.assertEqual(len(CATALOG), 17)

    def test_every_skill_has_bounded_contract(self):
        for name, spec in CATALOG.items():
            with self.subTest(name=name):
                self.assertEqual(name, spec.name)
                self.assertTrue(spec.role)
                self.assertGreater(spec.budget["wall_seconds"], 0)
                self.assertTrue(spec.output_kind)

    def test_every_skill_returns_common_envelope(self):
        payloads = {
            "scope-research-context": {"question": "q", "goals": ["g"], "scope": {"domain": "d"}},
            "map-theory-fragment": {"sources": ["Sort: X\nClaim: c"]},
            "propose-theory-morphism": {"source_fragment": {"fragment_id": "a", "symbols": {}}, "target_fragment": {"fragment_id": "b", "symbols": {}}, "scope_map": {"r": "r"}},
            "interpret-conceptual-pressure": {"events": ["proof blocker"]},
            "profile-concept-meaning": {"concept_id": "c", "theory_id": "t"},
            "detect-essential-fragmentation": {"profiles": [{"profile_id": "a", "concept_id": "c", "theory_id": "a"}, {"profile_id": "b", "concept_id": "c", "theory_id": "b"}]},
            "run-philosophical-reflection": {"site": {"site_id": "s", "concept_ids": ["c"], "theory_ids": ["a", "b"], "mismatch_vector": {"identity_criteria": 1.0}, "protected_losses": ["d"]}},
            "diagnose-categorical-defect": {"site": {"site_id": "s", "theory_ids": ["a", "b"], "mismatch_vector": {"identity_criteria": 1.0}}, "reflection": {"formal_obligations": ["o"]}},
            "generate-theory-candidates": {"pressures": [{"pressure_id": "p", "description": "gap"}]},
            "evaluate-relevance": {"candidate": BASE_CANDIDATE, "context": {"context_id": "q"}},
            "formalize-candidate": {"candidate": BASE_CANDIDATE},
            "prove-transport": {"morphism": {"morphism_id": "m", "total_on_declared_domain": True, "scope_map": {"a": "b"}, "obligations": []}, "theorems": []},
            "instantiate-concretely": {"candidate": BASE_CANDIDATE},
            "falsify-candidate": {"candidate": BASE_CANDIDATE},
            "mutate-representation": {"failures": [{"reason": "ill-typed"}, {"reason": "ill-typed"}]},
            "synthesize-portfolio": {"candidates": [BASE_CANDIDATE], "evaluations": [{"candidate_id": "c", "eligible": True, "relevance_vector": {key: .5 for key in ("unblocking", "explanatory", "unification", "predictive", "transport", "pragmatic", "necessity", "robustness")}, "penalties": {key: .2 for key in ("complexity", "fragility", "auxiliaries", "risk")}, "priority_index": .4}]},
            "audit-reasoning-run": {"trace": [{"skill_name": "x", "input_hash": "i", "result_hash": "o", "role": "r"}]},
        }
        for name, payload in payloads.items():
            with self.subTest(name=name):
                value = execute_skill(name, payload)
                validate_skill_result(value)

    def test_generator_cannot_validate_own_output(self):
        trace = [
            {"skill_name": "generate-theory-candidates", "input_hash": "i", "result_hash": "o", "role": "same", "candidate_id": "c"},
            {"skill_name": "formalize-candidate", "input_hash": "i2", "result_hash": "o2", "role": "same", "candidate_id": "c"},
        ]
        result = execute_skill("audit-reasoning-run", {"trace": trace})
        self.assertEqual(result["status"], "invalid")
        self.assertFalse(result["artifacts"][0]["checks"]["role_separation"])


if __name__ == "__main__":
    unittest.main()

