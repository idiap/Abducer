from fractions import Fraction as F
import unittest

from h6_typed_square_defects import (
    LinearMap,
    TypedTower,
    VectorSpace,
    balanced_star_certificate,
    calibration,
    characteristic_polynomial,
    counterexamples,
    identity,
    matrix_infinity_norm,
    polynomial_from_roots,
    q,
    random_rational_map,
    random_tower,
)

import random


class ExactTypedMapTests(unittest.TestCase):
    def test_fraction_only_guard(self):
        with self.assertRaises(TypeError):
            q(0.5)

    def test_space_requires_positive_dimension(self):
        with self.assertRaises(ValueError):
            VectorSpace("bad", 0)

    def test_map_shape_is_checked(self):
        x = VectorSpace("X", 2)
        y = VectorSpace("Y", 3)
        with self.assertRaises(ValueError):
            LinearMap.from_rows("bad", x, y, [[1, 0], [0, 1]])

    def test_named_types_not_dimensions_control_composition(self):
        x = VectorSpace("X", 2)
        y = VectorSpace("Y", 2)
        z = VectorSpace("Z", 2)
        a = identity(y, "a")
        b = LinearMap.from_rows("b", x, z, [[1, 0], [0, 1]])
        with self.assertRaises(TypeError):
            a.compose(b)

    def test_addition_checks_both_endpoint_types(self):
        x = VectorSpace("X", 2)
        y = VectorSpace("Y", 2)
        z = VectorSpace("Z", 2)
        a = LinearMap.from_rows("a", x, y, [[1, 0], [0, 1]])
        b = LinearMap.from_rows("b", x, z, [[1, 0], [0, 1]])
        with self.assertRaises(TypeError):
            a.add(b)

    def test_exact_induced_norms(self):
        x = VectorSpace("X", 2)
        a = LinearMap.from_rows("a", x, x, [[F(1, 3), F(-2, 3)], [2, F(1, 4)]])
        self.assertEqual(a.norm_infinity(), F(9, 4))
        self.assertEqual(a.norm_one(), F(7, 3))


class TelescopingIdentityTests(unittest.TestCase):
    dimensions = ([2, 3, 2, 2], [3, 2, 3, 2])

    def test_random_rational_towers_telescope_exactly(self):
        for seed in range(20):
            cert = random_tower(seed, *self.dimensions).telescoping_certificate()
            self.assertTrue(cert["identity_exact"], seed)
            self.assertTrue(cert["norm_bound_exactly_verified"], seed)

    def test_partial_tower_identity(self):
        tower = random_tower(51, *self.dimensions)
        for end in (1, 2, 3):
            self.assertTrue(tower.telescoping_certificate(end)["identity_exact"])

    def test_recovered_identity_exact_for_random_towers(self):
        for seed in range(10):
            tower = random_tower(seed + 100, *self.dimensions)
            recovery = random_rational_map(
                random.Random(seed + 500),
                "S3",
                tower.y_spaces[-1],
                tower.x_spaces[-1],
            )
            cert = tower.recovered_certificate(recovery)
            self.assertTrue(cert["identity_exact"], seed)
            self.assertTrue(cert["norm_bound_exactly_verified"], seed)

    def test_per_step_ledger_contains_exact_bounds(self):
        tower = random_tower(617, *self.dimensions)
        cert = tower.telescoping_certificate()
        self.assertEqual(len(cert["per_step_ledger"]), 3)
        for row in cert["per_step_ledger"]:
            self.assertLessEqual(F(row["term_norm"]), F(row["submultiplicative_bound"]))

    def test_tower_rejects_wrong_level_map(self):
        tower = random_tower(7, *self.dimensions)
        wrong_b = list(tower.b_maps)
        wrong_b[0] = LinearMap.from_rows(
            "wrong",
            VectorSpace("X0-alias", tower.x_spaces[0].dimension),
            tower.x_spaces[1],
            wrong_b[0].entries,
        )
        with self.assertRaises(TypeError):
            TypedTower(
                tower.x_spaces,
                tower.y_spaces,
                tuple(wrong_b),
                tower.t_maps,
                tower.r_maps,
            )

    def test_recovery_type_is_checked(self):
        tower = random_tower(7, *self.dimensions)
        wrong = identity(tower.x_spaces[-1])
        with self.assertRaises(TypeError):
            tower.recovered_certificate(wrong)


class BalancedStarTests(unittest.TestCase):
    def setUp(self):
        self.cert = balanced_star_certificate()

    def test_exact_commutator_rank_and_formula(self):
        self.assertTrue(self.cert["commutator_formula_exact"])
        self.assertEqual(self.cert["commutator_rank"], 2)

    def test_exact_euclidean_norm_certificate(self):
        self.assertTrue(self.cert["gram_is_rank_two_orthogonal_projector"])
        self.assertEqual(self.cert["euclidean_operator_norm"], "1")

    def test_correct_orientation_spectrum(self):
        self.assertEqual(
            self.cert["correct_orient_then_center_spectrum"],
            ["0", "239/630", "239/630", "33/70", "33/70", "33/70"],
        )
        self.assertTrue(self.cert["correct_characteristic_polynomial_exact"])

    def test_hostile_orientation_spectrum(self):
        self.assertEqual(
            self.cert["hostile_center_before_common_orientation_spectrum"],
            ["0", "239/630", "239/630", "33/70", "33/70", "1"],
        )
        self.assertTrue(self.cert["hostile_characteristic_polynomial_exact"])
        self.assertTrue(self.cert["spectra_differ"])

    def test_characteristic_polynomial_sanity(self):
        matrix = [[F(2), F(0)], [F(0), F(3)]]
        self.assertEqual(characteristic_polynomial(matrix), polynomial_from_roots([F(2), F(3)]))

    def test_geometric_provenance_fails_closed(self):
        self.assertFalse(
            self.cert["geometric_provenance_derived_or_hash_linked_in_stage73"]
        )
        self.assertEqual(len(self.cert["source_fixture_sha256"]), 64)


class MandatoryCounterexampleTests(unittest.TestCase):
    def setUp(self):
        self.models = counterexamples()

    def test_small_rotation_accumulates(self):
        model = self.models["small_rotations"]
        self.assertTrue(model["one_step_below_1_over_40"])
        self.assertTrue(model["accumulated_above_one"])

    def test_hidden_channel_becomes_visible(self):
        model = self.models["hidden_to_visible_swap"]
        self.assertTrue(model["currently_invisible"])
        self.assertTrue(model["later_visible_with_unit_amplitude"])

    def test_ill_conditioned_recovery_magnifies(self):
        model = self.models["ill_conditioned_recovery"]
        self.assertTrue(model["S_R_is_identity"])
        self.assertEqual(F(model["input_defect_infinity_norm"]), F(1, 1000))
        self.assertEqual(F(model["recovered_defect_infinity_norm"]), F(1))

    def test_support_multiplicity_reaches_order_one(self):
        model = self.models["support_multiplicity"]
        self.assertTrue(model["unit_accumulation"])
        self.assertEqual(
            model["support_size"] * F(model["per_cell_defect"]),
            F(model["unnormalized_sum_defect"]),
        )


class ClaimAuditTests(unittest.TestCase):
    def test_all_physical_guardrails_remain_false(self):
        self.assertTrue(all(value is False for value in calibration()["guardrails"].values()))

    def test_output_is_exactly_serializable(self):
        result = calibration()
        self.assertEqual(result["claim_level"].split()[0], "C2")
        self.assertTrue(
            result["typed_calibration"]["recovered_transport"]["identity_exact"]
        )


if __name__ == "__main__":
    unittest.main()
