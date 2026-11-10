from __future__ import annotations

from fractions import Fraction as F
import json
import unittest

import numpy as np

import exact_multistar as em


class ExactMultistarTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = em.build_results()

    def test_ambient_counts_and_rank(self) -> None:
        block = self.data["ambient_block"]
        self.assertEqual((block["vertices"], block["links"], block["plaquettes"]), (81, 216, 216))
        self.assertEqual(block["interior_links"], 8)
        self.assertEqual(block["d1_rank_over_Q"], 136)

    def test_orient_before_center_root_column_vanishes(self) -> None:
        d1, _, _, _ = em.block_incidence()
        link = em.interior_links(d1)[0]
        operator, _ = em.oriented_star_operator(d1, link)
        self.assertTrue(np.all(operator[:, link] == 0))

    def test_operator_hashes_are_distinct(self) -> None:
        hashes = [certificate["operator_sha256"] for certificate in self.data["certificates"].values()]
        self.assertEqual(len(set(hashes)), 3)

    def test_adjacent_pair_exact_spectrum(self) -> None:
        cert = self.data["certificates"]["adjacent_pair"]
        self.assertEqual((cert["star_data_rank_over_Q"], cert["spill_cost_rank_over_Q"], cert["spill_nullity_over_Q"]), (10, 10, 0))
        self.assertEqual(
            cert["certified_rational_factors"],
            [
                {"root": "16/19", "multiplicity": 3},
                {"root": "5/4", "multiplicity": 2},
                {"root": "3/2", "multiplicity": 3},
                {"root": "24/11", "multiplicity": 2},
            ],
        )
        self.assertEqual(cert["residual_characteristic_factor_low_first"], ["1/101559956668416"])

    def test_central_four_exact_nullity(self) -> None:
        cert = self.data["certificates"]["central_four"]
        self.assertEqual((cert["star_data_rank_over_Q"], cert["spill_cost_rank_over_Q"], cert["spill_nullity_over_Q"]), (18, 14, 4))
        self.assertEqual(len(cert["kernel_witnesses_in_row_coordinates"]), 4)

    def test_central_four_quartic_cube(self) -> None:
        algebraic = self.data["certificates"]["central_four"]["residual_algebraic_factorization"]
        self.assertTrue(algebraic["perfect_cube_identity_verified_over_Q"])
        self.assertEqual(algebraic["multiplicity"], 3)
        self.assertEqual(
            algebraic["quartic_low_first"],
            ["5696/1959", "-1045934/99909", "15120541/1198908", "-603718/99909", "1"],
        )

    def test_central_four_sturm_isolation(self) -> None:
        algebraic = self.data["certificates"]["central_four"]["residual_algebraic_factorization"]
        self.assertTrue(algebraic["four_distinct_positive_real_roots_verified_by_sturm"])
        self.assertEqual([item["root_count_by_sturm"] for item in algebraic["rational_isolating_intervals"]], [1, 1, 1, 1])

    def test_all_eight_exact_spectrum(self) -> None:
        cert = self.data["certificates"]["all_eight"]
        self.assertEqual((cert["star_data_rank_over_Q"], cert["spill_cost_rank_over_Q"], cert["spill_nullity_over_Q"]), (24, 17, 7))
        self.assertEqual(
            cert["certified_rational_factors"],
            [
                {"root": "0", "multiplicity": 7},
                {"root": "3/4", "multiplicity": 6},
                {"root": "12/11", "multiplicity": 8},
                {"root": "10/7", "multiplicity": 3},
            ],
        )

    def test_kernel_witnesses_substitute_exactly(self) -> None:
        for cert in self.data["certificates"].values():
            cost = [[F(value) for value in row] for row in cert["minimum_cost_matrix"]]
            for witness in cert["kernel_witnesses_in_row_coordinates"]:
                self.assertTrue(any(witness))
                self.assertEqual(
                    [sum((cost[i][j] * witness[j] for j in range(len(witness))), F(0)) for i in range(len(cost))],
                    [F(0)] * len(cost),
                )

    def test_complete_kkt_and_characteristic_checks(self) -> None:
        for cert in self.data["certificates"].values():
            self.assertTrue(cert["complete_kkt_system_verified_over_Q"])
            self.assertTrue(cert["characteristic_polynomial_verified_over_Q"])
            self.assertTrue(cert["kernel_witnesses_verified_over_Q"])

    def test_hostile_orientation_regression(self) -> None:
        regression = self.data["orientation_hostile_regression"]
        self.assertEqual(regression["correct_spill_nullity_over_Q"], 0)
        self.assertEqual(regression["hostile_spill_nullity_over_Q"], 1)
        self.assertEqual(regression["difference_rank_over_Q"], 2)
        self.assertTrue(regression["spurious_hostile_zero_mode_detected_exactly"])

    def test_guardrails(self) -> None:
        scope = self.data["scope"]
        self.assertFalse(scope["physical_boundary_law"])
        self.assertFalse(scope["nonlinear_gauge_covariant_repair"])
        self.assertFalse(scope["measure_or_partition_ratio"])
        self.assertFalse(scope["continuum_yang_mills"])
        self.assertFalse(scope["mass_gap"])

    def test_stored_certificate_matches_recomputation(self) -> None:
        stored = json.loads(em.RESULTS.read_text(encoding="utf-8"))
        self.assertEqual(stored, self.data)

    def test_invalid_root_rejected(self) -> None:
        d1, _, _, _ = em.block_incidence()
        with self.assertRaises(ValueError):
            em.oriented_star_operator(d1, 0)


if __name__ == "__main__":
    unittest.main()
