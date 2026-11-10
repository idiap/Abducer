import math
import unittest

from coherence_charge_tradeoff import (
    ALPHA,
    DEGREE,
    HEAT_TIME,
    calibration,
    coherent_eta_ceiling,
    contour_free_energy,
    eta_for_contour_target,
    eta_for_entropy_convergence,
    identical_witness_counterexample,
    maximum_degree_for_target,
    multi_witness_charge,
    rooted_free_energy_at_degree,
    tradeoff_certificate,
)


class CoherenceChargeTradeoffTests(unittest.TestCase):
    def test_disjoint_charge(self):
        cert = multi_witness_charge(4, 0.003, 1)
        self.assertAlmostEqual(cert.gibbs_exponent, 4 * 0.003**2 / (4 * HEAT_TIME))

    def test_overlap_reduces_charge(self):
        one = multi_witness_charge(6, 0.002, 1)
        three = multi_witness_charge(6, 0.002, 3)
        self.assertAlmostEqual(one.gibbs_exponent / three.gibbs_exponent, 3.0)

    def test_identical_witness_counterexample(self):
        data = identical_witness_counterexample(8)
        self.assertEqual(data["naive_overstatement_factor"], 8.0)
        self.assertFalse(data["additivity_without_overlap_control_valid"])

    def test_entropy_threshold_formula(self):
        eta = eta_for_entropy_convergence()
        exponent = eta**2 / (4 * HEAT_TIME)
        self.assertAlmostEqual(exponent, ALPHA + 2 * math.log(DEGREE), places=12)

    def test_below_entropy_threshold_diverges(self):
        eta = 0.999 * eta_for_entropy_convergence()
        self.assertFalse(contour_free_energy(eta).strict_entropy_convergence)

    def test_above_entropy_threshold_converges(self):
        eta = 1.01 * eta_for_entropy_convergence()
        self.assertTrue(contour_free_energy(eta).strict_entropy_convergence)

    def test_target_eta_meets_after_strict_move(self):
        eta = eta_for_contour_target()
        self.assertTrue(contour_free_energy(eta * (1 + 1e-8)).required_free_energy_met)

    def test_target_eta_fails_below(self):
        eta = eta_for_contour_target()
        self.assertFalse(contour_free_energy(eta * (1 - 1e-8)).required_free_energy_met)

    def test_larger_overlap_requires_larger_eta(self):
        self.assertGreater(eta_for_contour_target(overlap_multiplicity=2), eta_for_contour_target( overlap_multiplicity=1))

    def test_coherent_ceiling_finite(self):
        eta = coherent_eta_ceiling(0.022, 0.002)
        self.assertGreater(eta, 0.0)
        self.assertLess(eta, 0.022 / math.sqrt(6))

    def test_tradeoff_no_overlap_even_ideal_nu(self):
        cert = tradeoff_certificate(1)
        self.assertFalse(cert.common_eta_exists)
        self.assertLess(cert.feasible_interval_width, 0.0)

    def test_overlap_two_is_worse(self):
        one = tradeoff_certificate(1)
        two = tradeoff_certificate(2)
        self.assertGreater(two.minimum_coherence_radius_for_entropy_convergence, one.minimum_coherence_radius_for_entropy_convergence)
        self.assertLess(two.feasible_interval_width, one.feasible_interval_width)

    def test_repair_factors_are_nontrivial(self):
        cert = tradeoff_certificate(1)
        self.assertIsNotNone(cert.degree_reduction_factor_for_required_free_energy)
        self.assertGreater(cert.degree_reduction_factor_for_required_free_energy, 1.0)
        self.assertGreater(cert.charge_amplification_for_required_free_energy, 1.0)

    def test_required_free_energy_degree_is_stricter(self):
        cert = tradeoff_certificate(1)
        self.assertLess(
            cert.maximum_effective_degree_for_required_free_energy,
            cert.maximum_effective_degree_for_convergence,
        )

    def test_continuous_degree_target(self):
        cert = tradeoff_certificate(1)
        eta = cert.maximum_coherence_radius_accepted_by_coherent_bound
        degree = maximum_degree_for_target(eta, 6.712921011389365)
        self.assertIsNotNone(degree)
        self.assertAlmostEqual(
            rooted_free_energy_at_degree(eta, degree),
            6.712921011389365,
            places=10,
        )

    def test_overlap_two_needs_more_than_degree_repair(self):
        cert = tradeoff_certificate(2)
        self.assertFalse(cert.degree_only_repair_suffices_for_required_free_energy)
        self.assertIsNone(cert.maximum_effective_degree_for_required_free_energy)

    def test_claim_boundary(self):
        self.assertFalse(tradeoff_certificate().complete_measure_numerator_proved)

    def test_calibration(self):
        data = calibration()
        self.assertFalse(data["same_eta_closes_coherent_and_incoherent_channels"])
        self.assertFalse(data["volume_uniform_complete_su2_numerator_proved"])

    def test_invalid_overlap(self):
        with self.assertRaises(ValueError):
            multi_witness_charge(2, 0.001, 3)


if __name__ == "__main__":
    unittest.main()
