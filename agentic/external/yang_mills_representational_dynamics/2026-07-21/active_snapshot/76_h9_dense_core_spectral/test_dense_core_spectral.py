from __future__ import annotations

import math
import unittest

import numpy as np

import dense_core_spectral as dcs


class DenseCoreSpectralTests(unittest.TestCase):
    def setUp(self):
        self.h = np.diag([0.0, 0.4, 1.2])
        self.omega = np.array([1.0, 0.0, 0.0])

    def test_hidden_low_mode_reproduces_1_2_vs_0_4(self):
        cert = dcs.spectral_certificate(self.h, self.omega, [0.0, 0.0, 1.0])
        self.assertAlmostEqual(cert.true_gap, 0.4)
        self.assertAlmostEqual(cert.visible_gap, 1.2)
        self.assertEqual(cert.generated_invariant_rank, 1)
        self.assertFalse(cert.dense_in_vacuum_orthogonal)

    def test_dense_core_recovers_true_gap(self):
        cert = dcs.spectral_certificate(self.h, self.omega, np.eye(3)[:, 1:])
        self.assertAlmostEqual(cert.true_gap, 0.4)
        self.assertAlmostEqual(cert.visible_gap, 0.4)
        self.assertTrue(cert.dense_in_vacuum_orthogonal)
        self.assertTrue(cert.state_separating)

    def test_time_translates_enlarge_noninvariant_raw_span(self):
        cert = dcs.spectral_certificate(self.h, self.omega, [0.0, 1.0, 1.0])
        self.assertEqual(cert.raw_centered_probe_rank, 1)
        self.assertEqual(cert.generated_invariant_rank, 2)
        self.assertTrue(cert.dense_in_vacuum_orthogonal)

    def test_gap_equality_does_not_imply_density_at_multiplicity(self):
        fixture = dcs.multiplicity_fixture()["certificate"]
        self.assertAlmostEqual(fixture["true_gap"], 0.4)
        self.assertAlmostEqual(fixture["visible_gap"], 0.4)
        self.assertFalse(fixture["dense_in_vacuum_orthogonal"])
        self.assertEqual(fixture["invisible_spectral_dimensions"], 1)

    def test_hidden_core_bilinear_bound_is_restricted(self):
        cert = dcs.bilinear_decay_certificate(
            self.h, self.omega, [0.0, 0.0, 1.0], 1.2, [0, 0.5, 2]
        )
        self.assertTrue(cert.norm_compatible_checks_pass)
        self.assertFalse(cert.dense_extension)
        self.assertIsNone(cert.full_operator_norm_checks_pass)

    def test_dense_bilinear_bound_extends_to_full_operator_norm(self):
        cert = dcs.bilinear_decay_certificate(
            self.h, self.omega, np.eye(3)[:, 1:], 0.4, [0, 0.5, 2]
        )
        self.assertTrue(cert.norm_compatible_checks_pass)
        self.assertTrue(cert.dense_extension)
        self.assertTrue(cert.full_operator_norm_checks_pass)
        self.assertAlmostEqual(cert.generated_operator_norms[-1], math.exp(-0.8))

    def test_overaggressive_mass_fails_norm_check(self):
        cert = dcs.bilinear_decay_certificate(
            self.h, self.omega, np.eye(3)[:, 1:], 0.5, [1.0]
        )
        self.assertFalse(cert.norm_compatible_checks_pass)
        self.assertEqual(cert.conclusion, "the proposed decay rate is not certified")

    def test_zero_time_sample_cannot_certify_an_overaggressive_rate(self):
        cert = dcs.bilinear_decay_certificate(
            self.h, self.omega, np.eye(3)[:, 1:], 9.0, [0.0]
        )
        self.assertFalse(cert.norm_compatible_checks_pass)
        self.assertFalse(cert.full_operator_norm_checks_pass)
        self.assertEqual(cert.conclusion, "the proposed decay rate is not certified")

    def test_positive_transfer_recovers_physical_gap(self):
        transfer = dcs.transfer_from_hamiltonian(self.h, 0.25)
        cert = dcs.transfer_spectral_certificate(transfer, self.omega, 0.25)
        self.assertAlmostEqual(cert["physical_time_gap"], 0.4)
        self.assertTrue(cert["positive_self_adjoint_contraction"])

    def test_cutoff_family_has_positive_step_rates_but_collapses_physically(self):
        result = dcs.physical_time_collapse(8)
        self.assertTrue(result["all_step_exponents_positive"])
        self.assertTrue(result["physical_rates_strictly_decrease"])
        rates = [row["physical_time_gap"] for row in result["levels"]]
        self.assertAlmostEqual(rates[-1], 2.0 ** -7)
        self.assertEqual(result["limiting_physical_gap"], 0.0)

    def test_additional_zero_mode_reports_zero_true_gap(self):
        h = np.diag([0.0, 0.0, 1.0])
        cert = dcs.spectral_certificate(h, self.omega, np.eye(3)[:, 1:])
        self.assertEqual(cert.true_gap, 0.0)
        self.assertEqual(cert.visible_gap, 0.0)
        self.assertTrue(cert.dense_in_vacuum_orthogonal)

    def test_centering_removes_vacuum_component(self):
        cert = dcs.spectral_certificate(self.h, self.omega, [9.0, 1.0, 0.0])
        self.assertEqual(cert.raw_centered_probe_rank, 1)
        self.assertAlmostEqual(cert.visible_gap, 0.4)

    def test_nonselfadjoint_hamiltonian_rejected(self):
        with self.assertRaises(ValueError):
            dcs.spectral_certificate([[0, 1], [0, 1]], [1, 0], [0, 1])

    def test_negative_hamiltonian_rejected(self):
        with self.assertRaises(ValueError):
            dcs.spectral_certificate([[0, 0], [0, -1]], [1, 0], [0, 1])

    def test_bad_vacuum_rejected(self):
        with self.assertRaises(ValueError):
            dcs.spectral_certificate(self.h, [0, 1, 0], [0, 0, 1])
        with self.assertRaises(ValueError):
            dcs.spectral_certificate(self.h, [2, 0, 0], [0, 0, 1])

    def test_vacuum_only_probe_rejected(self):
        with self.assertRaises(ValueError):
            dcs.spectral_certificate(self.h, self.omega, self.omega)

    def test_nonfinite_and_bad_time_inputs_rejected(self):
        with self.assertRaises(ValueError):
            dcs.validate_hamiltonian([[0, 0], [0, math.inf]])
        with self.assertRaises(ValueError):
            dcs.semigroup(self.h, -1)
        with self.assertRaises(ValueError):
            dcs.bilinear_decay_certificate(self.h, self.omega, [0, 0, 1], 1.2, [])

    def test_signed_or_expansive_transfer_rejected(self):
        with self.assertRaises(ValueError):
            dcs.transfer_spectral_certificate(np.diag([1.0, -0.5]), [1, 0], 1.0)
        with self.assertRaises(ValueError):
            dcs.transfer_spectral_certificate(np.diag([1.0, 1.1]), [1, 0], 1.0)

    def test_nonselfadjoint_transfer_rejected(self):
        with self.assertRaises(ValueError):
            dcs.transfer_spectral_certificate([[1, 0.1], [0, 0.5]], [1, 0], 1.0)

    def test_scope_guardrails_remain_false(self):
        scope = dcs.results()["scope"]
        self.assertTrue(scope["finite_self_adjoint_theorem"])
        self.assertFalse(scope["os_reconstruction_constructed"])
        self.assertFalse(scope["continuum_theory_identity_established"])
        self.assertFalse(scope["continuum_yang_mills_mass_gap"])


if __name__ == "__main__":
    unittest.main()
