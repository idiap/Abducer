from __future__ import annotations

from fractions import Fraction as F
import json
import unittest

import numpy as np

from .exact_linear_algebra import (
    CERTIFICATE,
    block_incidence,
    build_certificate,
    determinant_pencil,
    interior_links,
)


class ExactLinearAlgebraTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = build_certificate()

    def test_block_counts(self) -> None:
        d1, vertices, edges, plaquettes = block_incidence()
        self.assertEqual((len(vertices), len(edges), len(plaquettes)), (81, 216, 216))
        self.assertEqual(len(interior_links(d1)), 8)
        self.assertTrue(np.all(np.sum(np.abs(d1), axis=1) == 4))

    def test_gaussian_spectrum(self) -> None:
        self.assertEqual(
            self.data["centered_gaussian_covariance"]["common_spectrum"],
            ["0", "239/630", "239/630", "33/70", "33/70", "33/70"],
        )
        self.assertTrue(all(c["normal_equations_verified_exactly"] for c in self.data["centered_gaussian_covariance"]["certificates"]))

    def test_spillover_spectrum(self) -> None:
        self.assertEqual(
            self.data["minimal_external_spillover"]["common_generalized_spectrum"],
            ["37/33", "37/33", "37/33", "391/239", "391/239"],
        )
        self.assertTrue(all(c["complete_kkt_system_verified_exactly"] for c in self.data["minimal_external_spillover"]["certificates"]))

    def test_polynomial_backend(self) -> None:
        metric = np.array([[F(1), F(0)], [F(0), F(1)]], dtype=object)
        cost = np.array([[F(2), F(0)], [F(0), F(3)]], dtype=object)
        self.assertEqual(determinant_pencil(metric, cost), [F(6), F(-5), F(1)])

    def test_stored_certificate(self) -> None:
        self.assertEqual(
            self.data,
            json.loads(CERTIFICATE.read_text(encoding="utf-8")),
        )


if __name__ == "__main__":
    unittest.main()
