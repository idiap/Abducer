import math
import unittest

import numpy as np

from center_contour_charging import (
    build_d2_gf2,
    center_complex_certificate,
    center_contour_certificate,
    frustration_charge_certificate,
    gf2_rank,
    link_plaquette_adjacency,
    plaquette_adjacency,
)


class CenterComplexTests(unittest.TestCase):
    def test_cell_counts_and_ranks(self):
        cert = center_complex_certificate()
        self.assertEqual((cert.links, cert.plaquettes, cert.three_cells), (216, 216, 96))
        self.assertEqual(cert.rank_d1_gf2, 136)
        self.assertEqual(cert.rank_d2_gf2, 80)

    def test_bianchi_and_exactness(self):
        cert = center_complex_certificate()
        self.assertTrue(cert.bianchi_composition_zero)
        self.assertTrue(cert.exact_at_plaquettes)
        self.assertEqual(cert.plaquette_exactness_dimension_sum, 216)

    def test_d2_has_six_faces_per_three_cell(self):
        _, d2 = build_d2_gf2()
        self.assertTrue(np.all(np.sum(d2, axis=1) == 6))

    def test_gf2_rank_is_stable_under_duplicate_row(self):
        _, d2 = build_d2_gf2()
        duplicated = np.vstack((d2, d2[0]))
        self.assertEqual(gf2_rank(duplicated), gf2_rank(d2))

    def test_adjacency_is_symmetric_and_loop_free(self):
        adjacency = plaquette_adjacency()
        for p, neighbors in enumerate(adjacency):
            self.assertNotIn(p, neighbors)
            for q in neighbors:
                self.assertIn(p, adjacency[q])

    def test_bianchi_and_link_adjacencies_are_distinguished(self):
        cert = center_complex_certificate()
        self.assertEqual(cert.link_adjacency_max_degree, 18)
        self.assertEqual(cert.bianchi_adjacency_max_degree, 20)
        self.assertEqual(max(map(len, link_plaquette_adjacency())), 18)


class FrustrationChargeTests(unittest.TestCase):
    def test_stage10_pattern_costs_exactly_five(self):
        cert = frustration_charge_certificate()
        self.assertTrue(cert.no_solution_weight_at_most_four)
        self.assertEqual(cert.exact_minimum_weight, 5)
        self.assertEqual(cert.candidate_weight, 5)

    def test_matching_candidate_has_one_negative_incident_target(self):
        cert = frustration_charge_certificate()
        self.assertIn(cert.target_plaquette_index, cert.candidate_negative_plaquettes)
        self.assertTrue(set(cert.forbidden_incident_plaquettes).isdisjoint(cert.candidate_negative_plaquettes))

    def test_nonempty_center_cocycle_minimum_is_three(self):
        self.assertEqual(frustration_charge_certificate().global_nonempty_center_cocycle_minimum, 3)

    def test_frustration_is_reported_as_charged(self):
        self.assertTrue(frustration_charge_certificate().target_pattern_charged)


class CenterContourTests(unittest.TestCase):
    def test_declared_center_weight_is_subcritical(self):
        cert = center_contour_certificate()
        self.assertTrue(cert.center_sector_convergent)
        self.assertLess(cert.branching_ratio, 1.0)
        self.assertLess(cert.rooted_weighted_contour_sum_upper, 1.0)
        self.assertEqual(cert.adjacency_degree, 20)

    def test_threshold_matches_counting_formula(self):
        cert = center_contour_certificate()
        expected = math.exp(-cert.alpha) / cert.adjacency_degree**2
        self.assertAlmostEqual(cert.convergence_threshold, expected)

    def test_target_factor_pays_five_plaquettes(self):
        cert = center_contour_certificate(2.0e-4)
        self.assertAlmostEqual(cert.least_suppressed_target_factor, (2.0e-4) ** 5)

    def test_supercritical_weight_fails_closed(self):
        threshold = center_contour_certificate().convergence_threshold
        cert = center_contour_certificate(1.01 * threshold)
        self.assertFalse(cert.center_sector_convergent)
        self.assertTrue(math.isinf(cert.rooted_weighted_contour_sum_upper))

    def test_invalid_inputs_fail_closed(self):
        for q in (0.0, 1.0, -0.1):
            with self.assertRaises(ValueError):
                center_contour_certificate(q)

    def test_no_false_continuous_measure_promotion(self):
        self.assertFalse(center_contour_certificate().continuous_su2_measure_certified)


if __name__ == "__main__":
    unittest.main()
