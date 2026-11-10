import math
import unittest

from uniform_vacuum_weight import (
    calibration,
    doob_kernel,
    harnack_certificate,
    inverse_partition_comparison,
    nonuniform_family,
    principal_vector,
    two_sector_transfer,
)


class UniformVacuumTests(unittest.TestCase):
    def test_perron_residual(self):
        _, _, residual = principal_vector([[1.0, 0.2], [0.3, 0.9]])
        self.assertLess(residual, 1e-12)

    def test_doob_rows(self):
        self.assertLess(doob_kernel([[1.0, 0.2], [0.3, 0.9]])["row_error"], 1e-12)

    def test_entrywise_harnack_bound(self):
        cert = harnack_certificate([[1.0, 0.2], [0.3, 0.9]])
        self.assertTrue(cert.bound_holds)
        self.assertLessEqual(cert.actual_amplitude_ratio, cert.entrywise_harnack_bound)

    def test_root_moment_is_controlled(self):
        cert = harnack_certificate([[1.0, 0.2], [0.3, 0.9]], [0.7, 0.3])
        self.assertLessEqual(cert.root_moment_upper, cert.entrywise_harnack_bound)

    def test_nonuniform_family_diverges(self):
        rows = nonuniform_family(20)
        self.assertGreater(rows[-1]["actual_ratio"], 1e8)
        self.assertGreater(rows[-1]["entrywise_bound"], 1e16)
        self.assertGreater(rows[-1]["root_moment"], 1e8)

    def test_two_sector_entries_are_positive(self):
        self.assertTrue(all(x > 0.0 for row in two_sector_transfer(10) for x in row))

    def test_nonpositive_matrix_rejected(self):
        with self.assertRaises(ValueError):
            principal_vector([[1.0, 0.0], [0.2, 1.0]])

    def test_bad_root_law_rejected(self):
        with self.assertRaises(ValueError):
            harnack_certificate([[1.0, 0.2], [0.2, 1.0]], [1.0, 1.0])

    def test_partition_comparison_detects_mismatch(self):
        out = inverse_partition_comparison([1.0, 0.5], [1.0, 1.0])
        self.assertAlmostEqual(out["comparison_factor"], 2.0)

    def test_guardrails(self):
        self.assertFalse(any(calibration()["guardrails"].values()))


if __name__ == "__main__":
    unittest.main()
