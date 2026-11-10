from fractions import Fraction as F
import json
from pathlib import Path
import tempfile
import unittest

from supplement.exact_enclosures import (
    SCHEMA, build_certificate, exp_negative_interval, exp_positive_interval,
    geometric_derivative_upper, image_derivative_upper, log_derivative_upper,
    normalized_tail_upper, partial_bell, pi_interval, sin_interval, sqrt_interval,
    transition_image_derivative_upper, write_certificate,
)
from supplement.verify_certificate import crosscheck_formulas, verify


class HeatKernelEnclosureTests(unittest.TestCase):
    def test_pi_enclosure_is_tight(self):
        lo, hi = pi_interval()
        self.assertLess(F(333, 106), lo)
        self.assertLess(hi, F(355, 113))
        self.assertLess(hi - lo, F(1, 10**45))

    def test_exp_negative_encloses_known_value(self):
        lo, hi = exp_negative_interval(F(1))
        self.assertLess(lo, F(367880, 10**6))
        self.assertLess(F(367879, 10**6), hi)

    def test_exp_positive_encloses_known_value(self):
        lo, hi = exp_positive_interval(F(1, 10))
        self.assertLess(lo, F(1105171, 10**6))
        self.assertLess(F(1105170, 10**6), hi)

    def test_sin_and_sqrt_primitives(self):
        lo, hi = sin_interval(F(1))
        self.assertLess(lo, F(841471, 10**6))
        self.assertLess(F(841470, 10**6), hi)
        slo, shi = sqrt_interval(F(2))
        self.assertLessEqual(slo * slo, 2)
        self.assertLessEqual(2, shi * shi)

    def test_image_hierarchy_contracts(self):
        for order in range(9):
            q, ratio = image_derivative_upper(order, F(1, 5), F(1))
            self.assertGreater(q, 0)
            self.assertLess(ratio, 1)

    def test_positive_kernel_floor(self):
        self.assertTrue(build_certificate()["passes"]["Q0_below_one"])

    def test_transition_kernel_floor(self):
        values = [
            transition_image_derivative_upper(m, F(1, 5), F(1, 5))[0]
            for m in range(9)
        ]
        self.assertLess(values[0], 1)
        self.assertTrue(all(v > 0 for v in values))

    def test_formula_adaptive_domain_cover(self):
        doc = build_certificate()
        self.assertTrue(doc["domain_cover"]["coverage_certified"])
        self.assertEqual([c["name"] for c in doc["domain_cover"]["cells"]],
                         ["identity", "transition", "cut_locus"])

    def test_bell_low_orders(self):
        xs = [F(2), F(3), F(5)]
        self.assertEqual(partial_bell(3, 1, xs), 5)
        self.assertEqual(partial_bell(3, 2, xs), 18)
        self.assertEqual(partial_bell(3, 3, xs), 8)

    def test_log_bounds_low_order_identities(self):
        qs = [F(1, 10), F(1, 5), F(1, 4), F(1, 3)]
        d = F(9, 10)
        self.assertEqual(log_derivative_upper(1, qs), qs[1] / d)
        self.assertEqual(log_derivative_upper(2, qs), qs[2] / d + qs[1] ** 2 / d ** 2)

    def test_geometric_hierarchy_positive(self):
        pi_lo, _ = pi_interval()
        self.assertTrue(all(geometric_derivative_upper(m, F(1), pi_lo) > 0
                            for m in range(1, 9)))

    def test_tail_improves_as_time_decreases(self):
        vals = [normalized_tail_upper(F(1, d), F(1)) for d in (5, 10, 20)]
        self.assertGreater(vals[0], vals[1])
        self.assertGreater(vals[1], vals[2])

    def test_invalid_tail_time_rejected(self):
        with self.assertRaises(ValueError):
            normalized_tail_upper(F(1, 4), F(1))

    def test_formula_crosscheck_including_endpoints(self):
        self.assertEqual(crosscheck_formulas()["cells"], 21)

    def test_certificate_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "certificate.json"
            doc = write_certificate(path)
            self.assertEqual(doc["schema"], SCHEMA)
            self.assertTrue(all(verify(path).values()))

    def test_tamper_is_detected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "certificate.json"
            write_certificate(path)
            doc = json.loads(path.read_text())
            doc["domain"]["radius"] = "2/1"
            path.write_text(json.dumps(doc))
            with self.assertRaises(AssertionError):
                verify(path)

    def test_hostile_order_and_time_gate(self):
        with self.assertRaises(ValueError):
            build_certificate(max_order=200, time_max=F(1, 5))

    def test_identity_and_cut_locus_chart_conditions(self):
        pi_lo, _ = pi_interval()
        self.assertGreater(pi_lo * pi_lo, F(1, 5) + pi_lo * F(1, 5))
        self.assertLess(F(1), pi_lo / 2)


if __name__ == "__main__":
    unittest.main()
