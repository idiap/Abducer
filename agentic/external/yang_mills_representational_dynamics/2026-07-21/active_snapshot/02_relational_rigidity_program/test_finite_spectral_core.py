from fractions import Fraction
import unittest

from finite_spectral_core import (
    FiniteHamiltonian,
    MorphismCertificate,
    RepresentationMorphism,
    SpectralMeasure,
    nonuniform_gap_sequence,
    observable_sector_is_complete,
    physical_gap,
)


class SpectralCoreTests(unittest.TestCase):
    def test_gapped_hamiltonian_decay_support(self):
        h = FiniteHamiltonian.diagonal([0, 2, 5])
        mu = h.spectral_measure([0, 3, 7])
        self.assertEqual(h.gap, 2)
        self.assertTrue(mu.certifies_decay_rate(2))
        self.assertFalse(mu.certifies_decay_rate(3))

    def test_low_energy_atom_is_detected(self):
        mu = SpectralMeasure.from_pairs([(Fraction(1, 3), 1), (2, 1)])
        self.assertTrue(mu.has_support_below(1))
        self.assertFalse(mu.certifies_decay_rate(1))

    def test_negative_spectral_weight_fails_closed(self):
        with self.assertRaises(ValueError):
            SpectralMeasure.from_pairs([(1, -1)])

    def test_nonunique_vacuum_fails_closed(self):
        with self.assertRaises(ValueError):
            FiniteHamiltonian.diagonal([0, 0, 1])

    def test_hidden_sector_is_not_complete(self):
        h = FiniteHamiltonian.diagonal([0, 1, Fraction(1, 1000)])
        visible_mu = h.spectral_measure([0, 1, 0])
        self.assertTrue(visible_mu.certifies_decay_rate(1))
        self.assertFalse(observable_sector_is_complete(h, [1]))
        self.assertEqual(h.gap, Fraction(1, 1000))

    def test_nonuniform_lattice_gap_collapses_physically(self):
        a, delta, m = nonuniform_gap_sequence(100)
        self.assertEqual(delta, Fraction(1, 10000))
        self.assertEqual(m, a)
        self.assertLess(m, Fraction(1, 10))

    def test_physical_unit_conversion(self):
        self.assertEqual(physical_gap(Fraction(1, 4), Fraction(1, 8)), 2)

    def test_morphism_composition_and_certificate_intersection(self):
        full = MorphismCertificate()
        loses_positivity = MorphismCertificate(reflection_positive=False)
        f = RepresentationMorphism("fine", "mid", Fraction(1, 100), full, ("block",))
        g = RepresentationMorphism("mid", "coarse", Fraction(1, 50), loses_positivity, ("truncate",))
        composed = f.compose(g)
        self.assertEqual(composed.error, Fraction(3, 100))
        self.assertEqual(composed.stages, ("block", "truncate"))
        self.assertEqual(composed.certificate.missing(), frozenset({"reflection_positive"}))
        self.assertTrue(composed.within(Fraction(3, 100)))
        self.assertFalse(composed.within(Fraction(1, 100)))

    def test_noncomposable_morphisms_fail(self):
        cert = MorphismCertificate()
        f = RepresentationMorphism.exact("A", "B", cert)
        g = RepresentationMorphism.exact("C", "D", cert)
        with self.assertRaises(ValueError):
            f.compose(g)


if __name__ == "__main__":
    unittest.main()
