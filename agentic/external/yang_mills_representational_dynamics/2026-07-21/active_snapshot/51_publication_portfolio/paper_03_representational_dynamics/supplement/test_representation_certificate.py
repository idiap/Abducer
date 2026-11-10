from fractions import Fraction as Q
import unittest

from supplement.representation_certificate import (
    CertificateProfile,
    FiniteSemigroup,
    RepresentationMorphism,
    finite_certificate,
    gapless_truncation,
    recovery_defect,
    uniformly_gapped_truncation,
)


class RepresentationCertificateTests(unittest.TestCase):
    def test_invalid_exact_forgotten_overlap(self):
        with self.assertRaises(ValueError):
            CertificateProfile.make(exact={"p"}, forgotten={"p"})

    def test_recovery_requires_forgotten_channel(self):
        with self.assertRaises(ValueError):
            CertificateProfile.make(recovered={"p"})

    def test_typed_composition_error(self):
        first = CertificateProfile.make(errors={"obs": Q(1, 10)})
        second = CertificateProfile.make(
            errors={"obs": Q(1, 20)}, lipschitz={"obs": Q(3, 2)}
        )
        self.assertEqual(dict(first.compose(second).errors)["obs"], Q(1, 5))

    def test_exact_channels_intersect(self):
        first = CertificateProfile.make(exact={"gauge", "positive"})
        second = CertificateProfile.make(exact={"positive", "local"})
        self.assertEqual(first.compose(second).exact, frozenset({"positive"}))

    def test_recovery_is_not_exactness(self):
        first = CertificateProfile.make(forgotten={"local"}, recovered={"local"})
        second = CertificateProfile.make(exact={"local"})
        profile = first.compose(second)
        self.assertIn("local", profile.recovered)
        self.assertNotIn("local", profile.exact)

    def test_morphism_endpoint_guard(self):
        p = CertificateProfile.make()
        with self.assertRaises(ValueError):
            RepresentationMorphism("a", "b", p).compose(
                RepresentationMorphism("c", "d", p)
            )

    def test_uniformly_gapped_truncations(self):
        self.assertTrue(all(uniformly_gapped_truncation(n).gap == 1 for n in range(1, 20)))

    def test_positive_finite_gaps_can_collapse(self):
        gaps = [gapless_truncation(n).gap for n in range(1, 21)]
        self.assertTrue(all(gap is not None and gap > 0 for gap in gaps))
        self.assertEqual(gaps[-1], Q(1, 20))

    def test_no_uniform_floor_for_gapless_chain(self):
        for numerator, denominator in ((1, 2), (1, 7), (2, 19)):
            m = Q(numerator, denominator)
            n = denominator // numerator + 1
            self.assertLess(gapless_truncation(n).gap, m)

    def test_hidden_sector(self):
        h = FiniteSemigroup.diagonal([0, 1, Q(1, 2)])
        self.assertEqual(h.visible_gap({1}), 1)
        self.assertEqual(h.gap, Q(1, 2))
        self.assertFalse(h.is_complete({1}))

    def test_pointwise_recovery_defect(self):
        for volume in range(1, 20):
            self.assertEqual(recovery_defect(volume, volume), 0)

    def test_nonuniform_volume_defect(self):
        for cutoff in range(1, 20):
            self.assertEqual(recovery_defect(cutoff, cutoff + 1), 1)

    def test_full_certificate(self):
        self.assertTrue(finite_certificate()["all_checks_pass"])


if __name__ == "__main__":
    unittest.main()
