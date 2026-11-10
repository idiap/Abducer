import math
import unittest

from weight_cocycle_physical_length import (
    Q_TARGET,
    calibration,
    cocycle_certificate,
    geometric_level_counterexample,
    mass_scaled_cocycle,
    physical_length_certificate,
    two_state_kernel,
    two_state_weight,
)


class WeightCocycleTests(unittest.TestCase):
    def test_six_step_cocycle_bound(self):
        out = cocycle_certificate([two_state_kernel(Q_TARGET)] * 6, [two_state_weight(Q_TARGET)] * 7, [1.0, 0.0])
        self.assertTrue(out.bound_holds)
        self.assertAlmostEqual(out.product_ceiling, Q_TARGET**6, places=28)

    def test_root_moment_is_retained(self):
        out = cocycle_certificate([two_state_kernel(Q_TARGET)], [two_state_weight(Q_TARGET)] * 2, [0.5, 0.5])
        self.assertGreater(out.root_moment, 1.0)

    def test_changing_rectangular_state_spaces(self):
        kernels = [[[0.1, 0.2, 0.0], [0.0, 0.1, 0.1]], [[0.2], [0.1], [0.3]]]
        weights = [[1.0, 1.0], [1.0, 1.0, 1.0], [1.0]]
        out = cocycle_certificate(kernels, weights, [1.0, 0.0])
        self.assertTrue(out.bound_holds)

    def test_superprobability_rejected(self):
        with self.assertRaises(ValueError):
            cocycle_certificate([[[1.1]]], [[1.0], [1.0]], [1.0])

    def test_weight_below_one_rejected(self):
        with self.assertRaises(ValueError):
            cocycle_certificate([[[0.2]]], [[1.0], [0.5]], [1.0])

    def test_physical_mass_formula(self):
        out = physical_length_certificate([math.exp(-0.3), math.exp(-0.6)], [1.0, 2.0])
        self.assertAlmostEqual(out["effective_mass"], 0.3, places=14)

    def test_constant_level_contraction_loses_mass(self):
        out = geometric_level_counterexample(20)
        self.assertLess(out["last_effective_mass"], 0.001)

    def test_constant_level_contraction_is_power_law(self):
        out = geometric_level_counterexample(10, 2.0, Q_TARGET)
        self.assertAlmostEqual(Q_TARGET**10, (2.0**10) ** (-out["power_law_exponent"]), places=25)

    def test_mass_scaled_cocycle_preserves_mass(self):
        self.assertLess(mass_scaled_cocycle()["mass_error"], 1e-14)

    def test_invalid_physical_lengths_rejected(self):
        with self.assertRaises(ValueError):
            physical_length_certificate([0.2], [0.0])

    def test_guardrails(self):
        self.assertFalse(any(calibration()["guardrails"].values()))


if __name__ == "__main__":
    unittest.main()
