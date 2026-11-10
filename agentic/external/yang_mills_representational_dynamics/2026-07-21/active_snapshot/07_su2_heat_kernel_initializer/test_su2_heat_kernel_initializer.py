import math
import unittest

from su2_heat_kernel_initializer import (
    ChartNorm,
    calibration,
    character_tail_probability,
    compose_with_curvature_chart,
    heat_kernel_local_certificate,
    image_derivative_bounds,
    su2_character_kernel,
    su2_image_kernel_shape,
)


class SU2HeatKernelInitializerTests(unittest.TestCase):
    def test_character_and_image_representations_agree_in_ratio(self):
        time = 0.2
        character_zero = su2_character_kernel(0.0, time, 80)
        image_zero = su2_image_kernel_shape(0.0, time, 4)
        for theta in (0.2, 0.6, 1.0):
            character_ratio = su2_character_kernel(theta, time, 80) / character_zero
            image_ratio = su2_image_kernel_shape(theta, time, 4) / image_zero
            self.assertAlmostEqual(character_ratio, image_ratio, places=12)

    def test_local_certificate_is_explicit_and_small(self):
        result = heat_kernel_local_certificate(0.2, 1.0, 1)
        self.assertLess(result.image_bounds.q0, 1e-20)
        self.assertLess(result.scaled_hessian_remainder_bound, 0.1)
        self.assertLess(result.scaled_third_derivative_bound, 0.2)

    def test_smaller_time_improves_local_budgets(self):
        coarse = heat_kernel_local_certificate(0.2, 1.0, 1)
        fine = heat_kernel_local_certificate(0.1, 1.0, 1)
        self.assertLess(fine.scaled_hessian_remainder_bound, coarse.scaled_hessian_remainder_bound)
        self.assertLess(fine.scaled_third_derivative_bound, coarse.scaled_third_derivative_bound)

    def test_image_tail_is_included(self):
        result = image_derivative_bounds(0.2, 1.0, 1)
        self.assertTrue(all(x > 0.0 for x in result.omitted_tail_bounds))
        self.assertTrue(all(math.isfinite(x) for x in result.omitted_tail_log_bounds))
        self.assertGreater(result.q3, result.omitted_tail_bounds[3])

    def test_cut_locus_neighborhood_is_rejected(self):
        with self.assertRaises(ValueError):
            heat_kernel_local_certificate(0.2, math.pi / 2.0, 1)

    def test_excessive_time_range_is_rejected(self):
        with self.assertRaises(ValueError):
            heat_kernel_local_certificate(5.0, 1.0, 1)

    def test_character_tail_interval_contains_reference(self):
        certificate = character_tail_probability(0.1, 1.0, 40)
        reference = character_tail_probability(0.1, 1.0, 100).partial_sum
        self.assertLessEqual(certificate.lower, reference)
        self.assertGreaterEqual(certificate.upper, reference)

    def test_tail_event_is_normalized_at_zero_radius(self):
        result = character_tail_probability(0.1, 0.0, 40)
        self.assertLessEqual(result.lower, 1.0)
        self.assertGreaterEqual(result.upper, 1.0)

    def test_tail_probability_decreases_with_radius(self):
        small = character_tail_probability(0.1, 0.75, 80)
        large = character_tail_probability(0.1, 1.0, 80)
        self.assertGreater(small.lower, large.upper)

    def test_reported_weak_coupling_tail_values_are_ordered(self):
        values = [
            character_tail_probability(t, 1.0, 80).partial_sum
            for t in (0.05, 0.1, 0.2)
        ]
        self.assertLess(values[0], values[1])
        self.assertLess(values[1], values[2])

    def test_identity_chart_preserves_curvature_budgets(self):
        local = heat_kernel_local_certificate(0.2, 1.0, 1)
        result = compose_with_curvature_chart(
            local, ChartNorm(1.0, 1.0, 0.0, 0.0, 0.0)
        )
        self.assertAlmostEqual(
            result.per_plaquette_hessian_budget,
            local.scaled_hessian_remainder_bound,
        )
        self.assertAlmostEqual(
            result.per_plaquette_third_budget,
            local.scaled_third_derivative_bound,
        )

    def test_nonlinear_chart_cost_is_exposed(self):
        local = heat_kernel_local_certificate(0.2, 1.0, 1)
        identity = compose_with_curvature_chart(
            local, ChartNorm(1.0, 1.0, 0.0, 0.0, 0.0)
        )
        nonlinear = compose_with_curvature_chart(
            local, ChartNorm(1.0, 1.1, 0.1, 0.2, 0.3), 6.0
        )
        self.assertGreater(
            nonlinear.aggregated_hessian_budget,
            identity.aggregated_hessian_budget,
        )

    def test_invalid_chart_or_aggregation_fails_closed(self):
        local = heat_kernel_local_certificate(0.2, 1.0, 1)
        with self.assertRaises(ValueError):
            ChartNorm(1.0, -1.0, 0.0, 0.0, 0.0)
        with self.assertRaises(ValueError):
            compose_with_curvature_chart(
                local, ChartNorm(1.0, 1.0, 0.0, 0.0, 0.0), 0.0
            )

    def test_calibration_schema_and_roundoff_audit(self):
        result = calibration()
        self.assertEqual(len(result["local_certificates"]), 2)
        self.assertEqual(len(result["tail_probabilities"]), 3)
        self.assertTrue(
            all(
                item["floating_roundoff_allowance"] > 0.0
                for item in result["tail_probabilities"]
            )
        )


if __name__ == "__main__":
    unittest.main()
