import math
import unittest

from two_plaquette_bridge import (
    bridge_density,
    bridge_lipschitz_coefficient,
    centered_bridge_defect_tail,
    connected_bad_cluster_bound,
    density_grid,
    gaussian_bridge_tail,
    product_block_tv_upper,
)


class TwoPlaquetteBridgeTests(unittest.TestCase):
    def test_bridge_density_normalizes(self):
        values, dx = density_grid(
            lambda q: bridge_density(q, 0.2, 0.3),
            4096,
        )
        self.assertAlmostEqual(dx * sum(values), 1.0, places=10)

    def test_full_mode_tends_to_half_response(self):
        t = 0.05
        delta = 0.1 * math.sqrt(t)
        coefficient = bridge_lipschitz_coefficient(t, 0.0, delta, False, 4096)
        self.assertAlmostEqual(coefficient, 0.5, delta=0.02)

    def test_centered_fiber_response_is_small(self):
        t = 0.05
        delta = 0.1 * math.sqrt(t)
        coefficient = bridge_lipschitz_coefficient(t, 0.0, delta, True, 4096)
        self.assertLess(coefficient, 0.01)

    def test_bridge_tail_approaches_gaussian_tail(self):
        observed = centered_bridge_defect_tail(0.05, 0.0, 3.0, 8192)
        expected = gaussian_bridge_tail(3.0)
        self.assertAlmostEqual(observed, expected, delta=0.0005)

    def test_degree_eight_gaussian_defects_are_subcritical_at_rho_three(self):
        branching = 64.0 * gaussian_bridge_tail(3.0)
        self.assertLess(branching, 1.0)

    def test_connected_cluster_bound_decays_when_subcritical(self):
        p = gaussian_bridge_tail(3.0)
        bounds = [connected_bad_cluster_bound(p, 8, n) for n in range(1, 6)]
        self.assertTrue(all(a > b for a, b in zip(bounds, bounds[1:])))

    def test_product_tv_tensorization(self):
        self.assertAlmostEqual(product_block_tv_upper(0.01, 16), 0.16)
        self.assertEqual(product_block_tv_upper(0.1, 16), 1.0)

    def test_invalid_inputs_fail_closed(self):
        with self.assertRaises(ValueError):
            connected_bad_cluster_bound(-0.1, 8, 1)
        with self.assertRaises(ValueError):
            product_block_tv_upper(0.1, 0)


if __name__ == "__main__":
    unittest.main()
