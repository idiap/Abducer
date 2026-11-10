import math
import unittest

import numpy as np

from one_step_effective_action import (
    DefectNorm,
    LocalActionNorm,
    calibration,
    gaussian_conditional_data,
    gaussian_effective_hessian,
    one_step_certificate,
    orthogonal_transform_blocks,
)


class OneStepEffectiveActionTests(unittest.TestCase):
    def test_small_certificate_closes(self):
        action = LocalActionNorm(0.25, 0.20, 0.10, 0.30, 0.20)
        defect = DefectNorm(0.01, 0.02, 0.03)
        result = one_step_certificate(2.0, 1.0, 0.5, action, defect)
        self.assertAlmostEqual(result.fiber_margin, 1.75)
        self.assertTrue(result.fiber_contraction_certified)
        self.assertTrue(result.generated_base_coercive)

    def test_fiber_budget_exhaustion_fails_closed(self):
        action = LocalActionNorm(2.0, 0.0, 0.0, 0.0, 0.0)
        with self.assertRaises(ValueError):
            one_step_certificate(2.0, 1.0, 0.1, action)

    def test_invalid_budget_fails_closed(self):
        with self.assertRaises(ValueError):
            LocalActionNorm(-0.1, 0.0, 0.0, 0.0, 0.0)
        with self.assertRaises(ValueError):
            DefectNorm(math.nan, 0.0, 0.0)

    def test_defect_budget_is_additive_after_log_bound(self):
        action = LocalActionNorm(0.2, 0.1, 0.05, 0.1, 0.1)
        defect = DefectNorm(0.2, 0.3, 0.4)
        result = one_step_certificate(2.0, 1.0, 0.2, action, defect)
        self.assertAlmostEqual(result.defect_hessian_budget, 0.49)
        self.assertAlmostEqual(
            result.generated_full_hessian_budget,
            result.generated_good_hessian_budget + 0.49,
        )

    def test_large_radius_rejects_contraction_without_corrupting_margin(self):
        action = LocalActionNorm(0.5, 0.5, 0.1, 3.0, 3.0)
        result = one_step_certificate(2.0, 1.0, 2.0, action)
        self.assertGreaterEqual(result.centered_transport_coefficient, 1.0)
        self.assertFalse(result.fiber_contraction_certified)
        self.assertGreater(result.fiber_margin, 0.0)

    def test_zero_base_curvature_is_not_reported_as_mass_generation(self):
        action = LocalActionNorm(0.2, 0.2, 0.1, 0.2, 0.2)
        result = one_step_certificate(2.0, 0.0, 0.2, action)
        self.assertFalse(result.generated_base_coercive)
        self.assertLess(result.generated_base_margin, 0.0)

    def test_gaussian_integration_is_schur_complement(self):
        base = np.array([[3.0, 0.2], [0.2, 2.0]])
        cross = np.array([[0.5, 0.1], [-0.2, 0.3]])
        fiber = np.array([[2.0, 0.1], [0.1, 1.5]])
        expected = base - cross @ np.linalg.inv(fiber) @ cross.T
        observed = gaussian_effective_hessian(base, cross, fiber)
        np.testing.assert_allclose(observed, expected, atol=1e-13)

    def test_gaussian_centered_covariance_is_base_independent(self):
        cross = np.array([[0.5, 0.1], [-0.2, 0.3]])
        fiber = np.array([[2.0, 0.1], [0.1, 1.5]])
        mean_map, covariance = gaussian_conditional_data(cross, fiber, 0.2)
        self.assertEqual(mean_map.shape, (2, 2))
        np.testing.assert_allclose(covariance, 0.2 * np.linalg.inv(fiber))

    def test_schur_complement_is_orthogonally_covariant(self):
        base = np.array([[3.0, 0.2], [0.2, 2.0]])
        cross = np.array([[0.5, 0.1], [-0.2, 0.3]])
        fiber = np.array([[2.0, 0.1], [0.1, 1.5]])
        qb = np.array([[0.0, -1.0], [1.0, 0.0]])
        qf = np.array([[1.0, 0.0], [0.0, -1.0]])
        transformed = orthogonal_transform_blocks(base, cross, fiber, qb, qf)
        lhs = gaussian_effective_hessian(*transformed)
        rhs = qb.T @ gaussian_effective_hessian(base, cross, fiber) @ qb
        np.testing.assert_allclose(lhs, rhs, atol=1e-13)

    def test_nonorthogonal_frame_fails_closed(self):
        base = np.eye(2)
        cross = np.zeros((2, 2))
        fiber = np.eye(2)
        with self.assertRaises(ValueError):
            orthogonal_transform_blocks(base, cross, fiber, 2.0 * np.eye(2), np.eye(2))

    def test_nonpositive_fiber_hessian_fails_closed(self):
        with self.assertRaises(ValueError):
            gaussian_effective_hessian(np.eye(1), np.zeros((1, 1)), -np.eye(1))

    def test_calibration_bound_and_schema(self):
        result = calibration()
        self.assertTrue(result["gaussian_witness"]["bound_respected"])
        self.assertEqual(result["input_from_stage_05"]["su2_fiber_dimension"], 357)
        self.assertEqual(len(result["certificate_examples"]), 3)


if __name__ == "__main__":
    unittest.main()
