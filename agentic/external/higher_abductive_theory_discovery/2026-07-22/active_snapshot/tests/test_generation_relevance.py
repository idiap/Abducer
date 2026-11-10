import unittest

from tdr.domain.models import jsonable
from tdr.generation import generate_candidates
from tdr.relevance import evaluate_candidate, pareto_frontier


def generated():
    return [jsonable(item) for item in generate_candidates({
        "pressures": [{"pressure_id": "p1", "description": "proof blocker"}],
        "reflections": [{"reflection_id": "r1"}],
        "defects": [{"kind": "coherence", "severity": 0.9, "required_objects": ["A", "B"], "required_morphisms": ["F"]}],
    })]


class GenerationRelevanceTests(unittest.TestCase):
    def test_generation_covers_all_modes_and_labels_conjectures(self):
        candidates = generated()
        self.assertEqual({item["mode"] for item in candidates}, {"local", "bridge", "mechanism", "mutation"})
        self.assertTrue(all(item["novelty_status"] == "conjectural" for item in candidates))
        self.assertTrue(all(item["validation_tasks"] for item in candidates))

    def test_relevance_gates_are_separate_and_not_truth_claim(self):
        evaluation = evaluate_candidate({"candidate": generated()[0], "context": {"context_id": "q"}})
        self.assertTrue(evaluation["eligible"])
        self.assertEqual(set(evaluation["gates"]), {"pressure", "leverage", "return"})
        self.assertIn("not evidence of truth", evaluation["epistemic_warning"])

    def test_absent_return_fails_gate(self):
        candidate = generated()[0]
        candidate["return_paths"] = []
        evaluation = evaluate_candidate({"candidate": candidate, "context": {"context_id": "q"}})
        self.assertFalse(evaluation["gates"]["return"]["passed"])
        self.assertFalse(evaluation["eligible"])

    def test_pareto_excludes_dominated_candidate(self):
        candidates = generated()[:2]
        better = evaluate_candidate({"candidate": candidates[0], "context": {"context_id": "q"}, "metrics": {
            "unblocking": 0.9, "explanatory": 0.9, "unification": 0.9, "predictive": 0.9,
            "transport": 0.9, "pragmatic": 0.9, "necessity": 0.9, "robustness": 0.9,
            "complexity": 0.1, "fragility": 0.1, "auxiliaries": 0.1, "risk": 0.1,
        }})
        worse = evaluate_candidate({"candidate": candidates[1], "context": {"context_id": "q"}, "metrics": {
            "unblocking": 0.2, "explanatory": 0.2, "unification": 0.2, "predictive": 0.2,
            "transport": 0.2, "pragmatic": 0.2, "necessity": 0.2, "robustness": 0.2,
            "complexity": 0.8, "fragility": 0.8, "auxiliaries": 0.8, "risk": 0.8,
        }})
        self.assertEqual([item["candidate_id"] for item in pareto_frontier([better, worse])], [better["candidate_id"]])


if __name__ == "__main__":
    unittest.main()

