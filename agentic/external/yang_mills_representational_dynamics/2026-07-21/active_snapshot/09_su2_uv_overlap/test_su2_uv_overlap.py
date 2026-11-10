import math
from pathlib import Path
import sys
import unittest


HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from su2_uv_overlap import (
    calibration,
    haar_jacobian_certificate,
    independent_polymer_certificate,
    search_overlap,
    su2_image_tail_upper,
    uv_overlap_certificate,
)


class HaarJacobianTests(unittest.TestCase):
    def test_origin_hessian_limit_is_two_thirds(self):
        cert = haar_jacobian_certificate(0.0)
        self.assertAlmostEqual(cert.hessian_operator_bound, 2.0 / 3.0, places=14)
        self.assertEqual(cert.third_derivative_operator_bound, 0.0)

    def test_bounds_increase_with_radius(self):
        small = haar_jacobian_certificate(0.004)
        large = haar_jacobian_certificate(0.01)
        self.assertLess(small.hessian_operator_bound, large.hessian_operator_bound)
        self.assertLess(
            small.third_derivative_operator_bound,
            large.third_derivative_operator_bound,
        )

    def test_cut_locus_radius_is_rejected(self):
        with self.assertRaises(ValueError):
            haar_jacobian_certificate(math.pi)


class ImageTailTests(unittest.TestCase):
    def test_witness_tail_is_small(self):
        cert = su2_image_tail_upper(3.0e-6, 0.0082)
        self.assertGreater(cert.normalization_lower, 0.0)
        self.assertLess(cert.probability_upper, 5.6e-5)
        self.assertGreater(cert.radius_in_heat_units, 4.7)

    def test_tail_decreases_with_radius(self):
        small = su2_image_tail_upper(3.0e-6, 0.0078)
        large = su2_image_tail_upper(3.0e-6, 0.0082)
        self.assertGreater(small.probability_upper, large.probability_upper)

    def test_tail_increases_with_heat_time_at_fixed_radius(self):
        cold = su2_image_tail_upper(2.5e-6, 0.0082)
        warm = su2_image_tail_upper(3.0e-6, 0.0082)
        self.assertLess(cold.probability_upper, warm.probability_upper)

    def test_character_cross_check_at_witness(self):
        stage07 = HERE.parent / "07_su2_heat_kernel_initializer"
        sys.path.insert(0, str(stage07))
        from su2_heat_kernel_initializer import character_tail_probability

        analytic = su2_image_tail_upper(3.0e-6, 0.0082)
        character = character_tail_probability(3.0e-6, 0.0082, 6000)
        self.assertLessEqual(character.upper, analytic.probability_upper)
        self.assertGreater(character.lower, 0.0)

    def test_invalid_tail_parameters_fail_closed(self):
        with self.assertRaises(ValueError):
            su2_image_tail_upper(0.0, 0.0082)
        with self.assertRaises(ValueError):
            su2_image_tail_upper(3.0e-6, math.pi)


class PolymerTests(unittest.TestCase):
    def test_witness_weighted_polymer_sum_is_subcritical(self):
        tail = su2_image_tail_upper(3.0e-6, 0.0082)
        cert = independent_polymer_certificate(tail.probability_upper)
        self.assertTrue(cert.weighted_subcritical)
        self.assertTrue(cert.rooted_sum_below_one)
        self.assertLess(cert.weighted_branching_proxy, 0.85)
        self.assertLess(cert.rooted_weighted_activity_sum_upper, 0.09)

    def test_stage08_scale_fails_independent_proxy(self):
        tail = su2_image_tail_upper(0.01, 0.006)
        cert = independent_polymer_certificate(tail.probability_upper)
        self.assertFalse(cert.weighted_subcritical)
        self.assertIsNone(cert.rooted_weighted_activity_sum_upper)

    def test_independence_is_explicit_hypothesis(self):
        cert = independent_polymer_certificate(1.0e-6)
        self.assertTrue(cert.independence_assumed)


class OverlapTests(unittest.TestCase):
    def test_default_witness_passes_all_restricted_inequalities(self):
        cert = uv_overlap_certificate()
        self.assertTrue(cert.local_action_certified)
        self.assertTrue(cert.independent_overlap_benchmark_certified)
        self.assertTrue(cert.strict_neighborhood_exists)
        self.assertLess(cert.augmented_hessian_remainder, 1.0)
        self.assertGreater(cert.generated_base_margin, 0.05)

    def test_haar_contribution_is_included_and_positive(self):
        cert = uv_overlap_certificate()
        self.assertGreater(cert.haar_scaled_hessian_contribution, 0.0)
        self.assertGreater(
            cert.augmented_hessian_remainder,
            cert.plaquette_hessian_remainder,
        )

    def test_no_false_full_measure_or_gap_promotion(self):
        cert = uv_overlap_certificate()
        self.assertFalse(cert.full_measure_certified)
        self.assertFalse(cert.dependent_polymer_certified)
        self.assertFalse(cert.topology_certified)
        self.assertFalse(cert.repeated_rg_certified)
        self.assertFalse(cert.continuum_certified)
        self.assertFalse(cert.mass_gap_certified)

    def test_stage08_point_does_not_overlap(self):
        cert = uv_overlap_certificate(0.01, 0.003, 0.001)
        self.assertTrue(cert.local_action_certified)
        self.assertFalse(cert.independent_overlap_benchmark_certified)

    def test_declared_search_finds_feasible_points_without_optimality_claim(self):
        cert = search_overlap(
            times=(2.5e-6, 3.0e-6, 3.5e-6),
            radii=(0.0040, 0.0041),
        )
        self.assertGreater(cert.feasible_points, 0)
        self.assertIsNotNone(cert.selected_time)
        self.assertFalse(cert.global_optimality_claimed)

    def test_calibration_names_first_unproved_implication(self):
        data = calibration()
        self.assertIn("dependent polymer", data["first_unproved_implication"])
        self.assertEqual(data["claim_level"], "C2 restricted certificate")


if __name__ == "__main__":
    unittest.main()
