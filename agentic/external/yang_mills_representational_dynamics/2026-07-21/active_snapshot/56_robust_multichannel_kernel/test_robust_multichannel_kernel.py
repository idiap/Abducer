import unittest

from robust_multichannel_kernel import (
    Q_CRITICAL,
    Q_TARGET,
    calibration,
    dominated_kernel_certificate,
    envelope_dominates,
    perron_certificate,
    persistence_budget,
    star_envelope,
    symmetric_radius,
    weighted_ceiling,
)


class RobustKernelTests(unittest.TestCase):
    def test_base_radius_is_target(self):
        cert = perron_certificate(star_envelope())
        self.assertAlmostEqual(cert.spectral_radius, Q_TARGET, places=12)

    def test_base_is_strictly_subcritical(self):
        self.assertTrue(perron_certificate(star_envelope()).strict_subcritical)

    def test_closed_form_with_persistence(self):
        p = 0.4 * persistence_budget()
        cert = perron_certificate(star_envelope(persistence=p))
        self.assertAlmostEqual(cert.spectral_radius, symmetric_radius(Q_TARGET, p), places=11)

    def test_persistence_boundary_hits_critical(self):
        p = persistence_budget()
        self.assertAlmostEqual(symmetric_radius(Q_TARGET, p), Q_CRITICAL, places=13)

    def test_half_budget_is_strict(self):
        p = 0.5 * persistence_budget()
        self.assertLess(perron_certificate(star_envelope(persistence=p)).weighted_ceiling, Q_CRITICAL)

    def test_entrywise_domination(self):
        envelope = star_envelope(persistence=0.25 * persistence_budget())
        candidate = [[0.8 * x for x in row] for row in envelope]
        out = dominated_kernel_certificate(candidate, envelope)
        self.assertTrue(out["bound_holds"])

    def test_nondominated_candidate_rejected(self):
        envelope = star_envelope()
        candidate = [row[:] for row in envelope]
        candidate[0][1] *= 1.1
        self.assertFalse(envelope_dominates(candidate, envelope))

    def test_cross_channel_mass_uses_same_budget(self):
        s = 0.4 * persistence_budget()
        a = perron_certificate(star_envelope(persistence=s)).spectral_radius
        b = perron_certificate(star_envelope(cross_total=s)).spectral_radius
        self.assertAlmostEqual(a, b, places=11)

    def test_invalid_superprobability_rejected(self):
        with self.assertRaises(ValueError):
            star_envelope(persistence=0.8, cross_total=0.3)

    def test_weight_validation(self):
        with self.assertRaises(ValueError):
            weighted_ceiling(star_envelope(), [1.0, 0.0, 1.0, 1.0, 1.0])

    def test_guardrails(self):
        self.assertFalse(any(calibration()["guardrails"].values()))


if __name__ == "__main__":
    unittest.main()
