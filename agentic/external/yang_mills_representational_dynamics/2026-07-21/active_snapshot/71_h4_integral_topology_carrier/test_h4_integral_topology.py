from fractions import Fraction
import itertools
import unittest

import h4_integral_topology as h4


class TestH4IntegralTopology(unittest.TestCase):
    def test_rejects_malformed_fluxes_and_bounds(self):
        for bad in ((0,) * 5, (0,) * 7, (0, 0, 0, 0, 0, True), (0, 0, 0, 0, 0, 1.0)):
            with self.assertRaises(ValueError):
                h4.validate_flux(bad)
        for bad_bound in (-1, 1.0, True):
            with self.assertRaises(ValueError):
                h4.validate_bound(bad_bound)  # type: ignore[arg-type]

    def test_pfaffian_and_covector(self):
        n = (2, -3, 5, 7, -11, 13)
        self.assertEqual(h4.pfaffian(n), 2 * 13 - (-3) * (-11) + 5 * 7)
        beta = h4.pairing_covector(n)
        self.assertEqual(h4.reconstruct_from_pairing_covector(beta), n)
        self.assertEqual(h4.context_signature(n, h4.standard_basis()), beta)

    def test_pairing_is_symmetric_and_polarizes_pfaffian_exhaustively(self):
        states = list(h4.flux_catalog(1))
        probes = states[::37] + list(h4.standard_basis())
        for left in states:
            for right in probes:
                self.assertEqual(h4.pairing(left, right), h4.pairing(right, left))
                self.assertEqual(h4.pfaffian(h4.add_flux(left, right)),
                                 h4.compose_charge(left, right))

    def test_pairing_matrix_exact_certificate(self):
        certificate = h4.pairing_certificate()
        self.assertTrue(certificate["J_squared_is_identity"])
        self.assertEqual(certificate["determinant"], -1)
        self.assertTrue(certificate["unimodular"])
        self.assertEqual(certificate["signature"], [3, 3])

    def test_mod_two_reduction_is_additive_exhaustively(self):
        states = list(h4.flux_catalog(1))
        self.assertEqual(len({h4.center_reduction(state) for state in states}), 64)
        probes = states[::41]
        for left in states:
            for right in probes:
                self.assertEqual(
                    h4.center_reduction(h4.add_flux(left, right)),
                    h4.center_add(left, right),
                )
                self.assertEqual(h4.pfaffian(left) % 2,
                                 sum((left[a] * left[b]) for a, b in ((0, 5), (1, 4), (2, 3))) % 2)

    def test_all_coordinate_permutations_have_orientation_law(self):
        samples = [(2, -3, 5, 7, -11, 13), (-1, 0, 1, 1, -1, 0)]
        for permutation in itertools.permutations(range(4)):
            for sample in samples:
                self.assertEqual(
                    h4.pfaffian(h4.relabel_flux(sample, permutation)),
                    h4.permutation_sign(permutation) * h4.pfaffian(sample),
                )

    def test_bad_permutations_rejected(self):
        for bad in ((0, 1, 2), (0, 1, 2, 4), (0, 0, 2, 3)):
            with self.assertRaises(ValueError):
                h4.permutation_sign(bad)

    def test_composition_is_associative(self):
        states = list(h4.flux_catalog(1))[::43]
        for left in states:
            for middle in states:
                for right in h4.standard_basis():
                    self.assertEqual(
                        h4.add_flux(h4.add_flux(left, middle), right),
                        h4.add_flux(left, h4.add_flux(middle, right)),
                    )
                    self.assertEqual(
                        h4.pfaffian(h4.add_flux(h4.add_flux(left, middle), right)),
                        h4.pfaffian(h4.add_flux(left, h4.add_flux(middle, right))),
                    )

    def test_one_cell_torus_full_smith_certificate(self):
        certificate = h4.one_cell_torus_certificate()
        self.assertEqual(certificate["cell_ranks"], [1, 4, 6, 4, 1])
        self.assertEqual(certificate["integral_betti_numbers"], [1, 4, 6, 4, 1])
        self.assertTrue(certificate["H2_is_Z6"])
        self.assertTrue(certificate["all_coboundaries_zero"])
        self.assertTrue(all(item["smith_nonzero_diagonal"] == []
                            for item in certificate["smith_normal_forms"]))

    def test_canonical_scalar_sector_collision(self):
        witness = h4.canonical_collision()
        self.assertEqual(witness["shared_charge"], 1)
        self.assertEqual(witness["left_composite_charge"], 0)
        self.assertEqual(witness["right_composite_charge"], 2)
        self.assertEqual(witness["shared_scalar_weight"], "1/2")
        self.assertEqual(witness["left_composite_scalar_weight"], "1")
        self.assertEqual(witness["right_composite_scalar_weight"], "1/4")

    def test_scalar_weight_rejects_nonexact_or_degenerate_fugacity(self):
        for bad in (0.5, Fraction(0), Fraction(1), Fraction(-1, 2)):
            with self.assertRaises(ValueError):
                h4.scalar_charge_weight(h4.ZERO_FLUX, bad)  # type: ignore[arg-type]

    def test_exhaustive_two_block_audit(self):
        audit = h4.exhaustive_two_block_audit(1)
        self.assertEqual(audit["state_count"], 729)
        self.assertEqual(audit["context_count"], 729)
        self.assertEqual(audit["state_context_compositions_checked"], 729 ** 2)
        self.assertGreater(audit["ambiguous_scalar_sector_count"], 0)
        self.assertEqual(audit["ambiguous_scalar_sector_count"],
                         audit["compositionally_ambiguous_scalar_sector_count"])
        self.assertTrue(audit["all_same_sector_pairs_distinguished_by_six_basis_contexts"])
        self.assertTrue(audit["full_flux_direct_equals_composed_for_every_pair"])
        self.assertFalse(audit["scalar_sector_admits_context_independent_composition"])

    def test_guardrails_fail_closed(self):
        guardrails = h4.calibration(0)["guardrails"]
        self.assertTrue(guardrails)
        self.assertFalse(any(guardrails.values()))


if __name__ == "__main__":
    unittest.main()
