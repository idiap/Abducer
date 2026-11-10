from __future__ import annotations

import unittest

from supplement.verify_incidence import build_certificate, dimension_certificate


class IncidenceCertificateTests(unittest.TestCase):
    def test_declared_dimension_range(self) -> None:
        certificate = build_certificate(2, 6)
        self.assertTrue(certificate["all_checks_pass"])
        self.assertEqual(certificate["dimension_range"], [2, 6])

    def test_exact_counts_in_four_dimensions(self) -> None:
        row = dimension_certificate(4)
        self.assertEqual(row["vertices"], 81)
        self.assertEqual(row["edges"], 216)
        self.assertEqual(row["plaquettes"], 216)
        self.assertEqual(row["incident_degree"], 6)
        self.assertEqual(row["gf2_rank"], 6)

    def test_identity_minor_all_dimensions(self) -> None:
        for dimension in range(2, 7):
            with self.subTest(dimension=dimension):
                row = dimension_certificate(dimension)
                self.assertTrue(row["private_opposites_distinct"])
                self.assertTrue(row["opposite_minor_is_identity"])
                self.assertTrue(row["surjective"])

    def test_order_reversal_preserves_rank(self) -> None:
        for dimension in range(2, 7):
            with self.subTest(dimension=dimension):
                row = dimension_certificate(dimension)
                self.assertEqual(row["gf2_rank"], row["reversed_order_gf2_rank"])

    def test_invalid_dimension_rejected(self) -> None:
        with self.assertRaises(ValueError):
            dimension_certificate(1)


if __name__ == "__main__":
    unittest.main()
