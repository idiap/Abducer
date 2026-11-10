import math
import unittest

from normalized_retained_kernel import (
    Q_TARGET,
    build_kernel,
    calibration,
    collapsed_normalizer_counterexample,
    covariance_error,
    four_channel_disintegration,
    relabel_table,
    weighted_bad_ratios,
)


class NormalizedKernelTests(unittest.TestCase):
    def setUp(self):
        self.w, self.t, self.b, self.v = four_channel_disintegration()

    def test_rows_are_normalized(self):
        cert = build_kernel(self.w, self.t, self.b)
        self.assertLess(max(cert.row_errors), 1e-14)

    def test_bad_kernel_is_subprobability(self):
        cert = build_kernel(self.w, self.t, self.b)
        self.assertLessEqual(max(cert.bad_row_masses), 1.0)

    def test_exact_partition_ratio_identity(self):
        out = weighted_bad_ratios(self.w, self.t, self.b, self.v)
        self.assertLess(out["identity_error"], 1e-15)

    def test_four_channel_weighted_ceiling(self):
        out = weighted_bad_ratios(self.w, self.t, self.b, self.v)
        self.assertAlmostEqual(out["weighted_ceiling"], Q_TARGET, places=15)

    def test_relabeling_covariance(self):
        p = [0, 3, 4, 1, 2]
        fp = [[0, 3, 4, 1, 2], [0], [0], [0], [0]]
        rw, rt, rb = relabel_table(self.w, self.t, self.b, p, fp)
        self.assertLess(covariance_error(build_kernel(self.w, self.t, self.b), build_kernel(rw, rt, rb), p), 1e-15)

    def test_nonpositive_fiber_weight_is_rejected(self):
        with self.assertRaises(ValueError):
            build_kernel([[0.0]], [[0]], [[False]])

    def test_invalid_state_weight_is_rejected(self):
        with self.assertRaises(ValueError):
            weighted_bad_ratios(self.w, self.t, self.b, [1.0] * 4)

    def test_action_only_counterexample(self):
        rows = collapsed_normalizer_counterexample(20)
        self.assertLess(rows[-1]["bad_weight"], 1e-8)
        self.assertGreater(rows[-1]["bad_probability"], 0.999999)

    def test_guardrails(self):
        guards = calibration()["guardrails"]
        self.assertFalse(any(guards.values()))


if __name__ == "__main__":
    unittest.main()
