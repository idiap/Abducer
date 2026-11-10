import unittest

from tdr.domain.models import jsonable
from tdr.pressures import dependency_impact, interpret_pressures
from tdr.reflection import detect_fragmentation, diagnose_defect, profile_meaning, run_reflection


def profile(concept, theory, token):
    return jsonable(profile_meaning({
        "concept_id": concept,
        "theory_id": theory,
        "referential_role": [f"{token} reference"],
        "inferential_commitments": [f"{token} inference"],
        "identity_criteria": [f"{token} identity"],
        "modal_commitments": [f"{token} modality"],
        "operational_anchors": [f"{token} operation"],
        "scale_and_scope": [f"{token} scope"],
        "explanatory_role": [f"{token} explanation"],
        "pragmatic_uses": [f"{token} use"],
        "protected_distinctions": [f"{token} distinction"],
    }))


class PressureReflectionTests(unittest.TestCase):
    def test_dependency_impact(self):
        impact = dependency_impact(["a", "b", "c", "d"], [["a", "b"], ["b", "c"]], ["a"])
        self.assertEqual(impact, 0.75)

    def test_pressure_does_not_hide_preferred_solution(self):
        item = interpret_pressures({"events": [{"description": "proof cannot derive lemma", "preferred_solution": "add adjoint"}]})[0]
        self.assertEqual(item.kind, "proof_blocker")
        self.assertEqual(item.preferred_solution, "add adjoint")

    def test_profile_marks_missing_components_unknown(self):
        value = profile_meaning({"concept_id": "mass", "theory_id": "T"})
        self.assertEqual(value.identity_criteria, ["unknown"])
        self.assertEqual(value.uncertainty["identity_criteria"], 1.0)

    def test_fragmentation_is_invariant_under_token_order(self):
        a = profile("c", "A", "left")
        b = profile("c", "B", "right")
        first = detect_fragmentation({"profiles": [a, b], "downstream_impact": 1.0})
        for key in ("referential_role", "inferential_commitments"):
            a[key] = list(reversed(a[key]))
            b[key] = list(reversed(b[key]))
        second = detect_fragmentation({"profiles": [a, b], "downstream_impact": 1.0})
        self.assertEqual(first.mismatch_vector, second.mismatch_vector)

    def test_reflection_has_plural_lenses_losses_and_counterworlds(self):
        a, b = profile("c", "A", "left"), profile("c", "B", "right")
        site = jsonable(detect_fragmentation({"profiles": [a, b], "downstream_impact": 1.0}))
        record = run_reflection({"site": site, "profiles": [a, b]})
        self.assertEqual(len(record.lens_outputs), 8)
        self.assertGreaterEqual(len(record.redescriptions), 3)
        self.assertTrue(record.anticipated_losses)
        self.assertTrue(record.counterworlds)
        defects = diagnose_defect({"site": site, "reflection": jsonable(record)})
        self.assertTrue(any(not item["metaphorical"] for item in defects))


if __name__ == "__main__":
    unittest.main()

