from fractions import Fraction as F
import unittest

from observable_recovery import (
    CHARACTER_BASIS,
    FINE_CONFIGS,
    GAUGE_GROUP,
    INITIAL_PROBES,
    ONE,
    QUOTIENT_CONFIGS,
    W01,
    W02,
    W12,
    InvariantObservable,
    QuotientMap,
    calibration,
    canonical_reconstruct,
    composition_certificate,
    counterexamples,
    exhaustive_composition_check,
    gauge_action,
    gauge_equivalent,
    gauge_orbit,
    gauge_quotient_certificate,
    observable_class_certificate,
    observable_error,
    quotient_block,
    quotient_observable_error,
    recovery_projection,
    validate_fine,
    validate_gauge,
    validate_quotient,
    wilson_02,
)


class TypedInputTests(unittest.TestCase):
    def test_invalid_fine_shape_and_sign_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_fine((1, -1))
        with self.assertRaises(ValueError):
            validate_fine((1, 0, -1))
        with self.assertRaises(ValueError):
            validate_fine((True, 1, -1))

    def test_invalid_gauge_and_quotient_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_gauge((1,))
        with self.assertRaises(ValueError):
            validate_gauge((1, 2))
        with self.assertRaises(ValueError):
            validate_quotient((1, -1, 1))
        with self.assertRaises(ValueError):
            validate_quotient((0, 1))

    def test_observable_rejects_floats_and_bad_coefficient_count(self):
        with self.assertRaises(TypeError):
            InvariantObservable.from_coefficients("bad", (0.5, 0, 0, 0))
        with self.assertRaises(ValueError):
            InvariantObservable.from_coefficients("bad", (1, 2))
        with self.assertRaises(ValueError):
            InvariantObservable.from_coefficients("", (1, 0, 0, 0))

    def test_quotient_map_rejects_missing_or_invalid_images(self):
        with self.assertRaises(ValueError):
            QuotientMap.from_mapping("missing", {QUOTIENT_CONFIGS[0]: (1, 1)})
        bad = {y: y for y in QUOTIENT_CONFIGS}
        bad[QUOTIENT_CONFIGS[0]] = (1, 0)
        with self.assertRaises(ValueError):
            QuotientMap.from_mapping("bad image", bad)


class GaugeQuotientTests(unittest.TestCase):
    def test_block_is_gauge_invariant_for_every_pair(self):
        for x in FINE_CONFIGS:
            for g in GAUGE_GROUP:
                self.assertEqual(quotient_block(gauge_action(g, x)), quotient_block(x))

    def test_every_fibre_is_exactly_one_effective_orbit(self):
        for y in QUOTIENT_CONFIGS:
            fibre = {x for x in FINE_CONFIGS if quotient_block(x) == y}
            self.assertEqual(len(fibre), 2)
            self.assertEqual(fibre, set(gauge_orbit(next(iter(fibre)))))

    def test_reconstruction_is_section_and_projection_is_orbit_equivalent(self):
        for y in QUOTIENT_CONFIGS:
            self.assertEqual(quotient_block(canonical_reconstruct(y)), y)
        for x in FINE_CONFIGS:
            self.assertTrue(gauge_equivalent(x, recovery_projection(x)))

    def test_projection_erases_every_gauge_copy(self):
        for x in FINE_CONFIGS:
            for g in GAUGE_GROUP:
                self.assertEqual(recovery_projection(gauge_action(g, x)), recovery_projection(x))

    def test_product_loop_identity(self):
        for x in FINE_CONFIGS:
            self.assertEqual(wilson_02(x), quotient_block(x)[0] * quotient_block(x)[1])

    def test_certificate_has_exact_counts(self):
        cert = gauge_quotient_certificate()
        self.assertEqual(cert["fine_configuration_count"], 8)
        self.assertEqual(cert["gauge_group_count"], 4)
        self.assertEqual(cert["effective_orbit_size"], 2)
        self.assertEqual(cert["quotient_count"], 4)
        self.assertTrue(cert["each_fibre_is_one_orbit"])


class ObservableAlgebraTests(unittest.TestCase):
    def test_character_basis_separates_and_spans(self):
        cert = observable_class_certificate()
        self.assertTrue(cert["separates_quotient_points"])
        self.assertEqual(cert["evaluation_matrix_rank"], 4)
        self.assertTrue(cert["basis_spans_all_rational_invariant_functions"])

    def test_character_basis_is_product_closed(self):
        cert = observable_class_certificate()
        self.assertTrue(cert["closed_under_products"])
        self.assertEqual(W01.multiply(W12).coefficients, W02.coefficients)
        self.assertEqual(W02.multiply(W02).coefficients, ONE.coefficients)

    def test_declared_coefficient_norm_is_submultiplicative(self):
        left = InvariantObservable.from_coefficients("left", (1, "-2/3", "1/7", 2))
        right = InvariantObservable.from_coefficients("right", ("3/5", 1, -2, "1/3"))
        self.assertLessEqual(
            left.multiply(right).coefficient_norm,
            left.coefficient_norm * right.coefficient_norm,
        )

    def test_every_declared_basis_observable_has_zero_recovery_error(self):
        for observable in CHARACTER_BASIS:
            error = observable_error(quotient_block, canonical_reconstruct, observable)
            self.assertEqual(F(error["linfinity_error"]), 0)
            self.assertEqual(F(error["l1_uniform_fine_error"]), 0)
            self.assertTrue(error["exact_recovery"])

    def test_product_outside_initial_probe_family_is_explicit(self):
        self.assertNotIn(W02, INITIAL_PROBES)
        self.assertTrue(
            observable_error(quotient_block, canonical_reconstruct, W02)["exact_recovery"]
        )


class CompositionTests(unittest.TestCase):
    def setUp(self):
        self.flip_first = QuotientMap.from_mapping(
            "flip first", {y: (-y[0], y[1]) for y in QUOTIENT_CONFIGS}
        )
        self.flip_second = QuotientMap.from_mapping(
            "flip second", {y: (y[0], -y[1]) for y in QUOTIENT_CONFIGS}
        )

    def test_one_step_indexed_errors(self):
        self.assertEqual(quotient_observable_error(self.flip_first, W01), 2)
        self.assertEqual(quotient_observable_error(self.flip_first, W12), 0)
        self.assertEqual(quotient_observable_error(self.flip_second, W01), 0)
        self.assertEqual(quotient_observable_error(self.flip_second, W12), 2)

    def test_two_step_triangle_bound_has_exact_equality_case(self):
        average = InvariantObservable.from_coefficients(
            "average", (0, "1/2", "1/2", 0)
        )
        cert = composition_certificate(self.flip_first, self.flip_second, average)
        self.assertEqual(F(cert["first_error"]), 1)
        self.assertEqual(F(cert["second_error"]), 1)
        self.assertEqual(F(cert["two_step_error"]), 2)
        self.assertEqual(F(cert["sum_bound"]), 2)
        self.assertTrue(cert["inequality_verified"])

    def test_exhaustive_two_step_check(self):
        cert = exhaustive_composition_check()
        self.assertEqual(cert["number_of_quotient_maps"], 256)
        self.assertEqual(cert["certified_map_pair_observable_triples"], 262144)
        self.assertTrue(cert["all_inequalities_verified"])
        self.assertEqual(F(cert["minimum_slack"]), 0)


class MandatoryCounterexampleTests(unittest.TestCase):
    def setUp(self):
        self.models = counterexamples()

    def test_erasure_does_not_imply_recovery(self):
        model = self.models["erasure_without_recovery"]
        self.assertTrue(model["block_is_gauge_invariant"])
        self.assertEqual(model["number_of_retained_physical_labels"], 1)
        self.assertEqual(model["number_of_true_orbits"], 4)
        self.assertTrue(model["recovery_fails"])
        self.assertEqual(F(model["observable_errors"][W01.name]["linfinity_error"]), 2)

    def test_recovery_does_not_imply_erasure(self):
        model = self.models["recovery_without_erasure"]
        self.assertTrue(model["R_labeled_after_B_labeled_is_fine_identity"])
        self.assertTrue(model["all_invariant_observables_exactly_recovered"])
        self.assertFalse(model["block_erases_gauge_copies"])
        self.assertTrue(model["retains_vertical_copy_label"])

    def test_small_probe_class_does_not_imply_full_recovery(self):
        model = self.models["incomplete_probe_class"]
        self.assertTrue(model["all_initial_probes_recovered"])
        self.assertTrue(model["separating_class_not_recovered"])
        self.assertEqual(F(model["hidden_W12_error"]), 2)
        self.assertEqual(F(model["product_W02_error"]), 2)


class ClaimAuditTests(unittest.TestCase):
    def test_claim_level_and_all_physical_guardrails(self):
        result = calibration(run_exhaustive=False)
        self.assertTrue(result["claim_level"].startswith("C2"))
        self.assertTrue(all(value is False for value in result["guardrails"].values()))

    def test_canonical_output_contains_required_observable_examples(self):
        result = calibration(run_exhaustive=False)
        examples = result["observable_indexed_examples"]
        self.assertIn("elementary_W01", examples)
        self.assertIn("elementary_W12", examples)
        self.assertIn("product_outside_initial_probe_family_W02", examples)


if __name__ == "__main__":
    unittest.main()
