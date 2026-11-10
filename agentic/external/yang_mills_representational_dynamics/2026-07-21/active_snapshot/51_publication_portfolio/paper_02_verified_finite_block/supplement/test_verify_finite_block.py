from fractions import Fraction as Q
import unittest

from supplement.verify_finite_block import (
    analytic_budgets,
    block_complex,
    certificate,
    exact_ldlt_floor,
    gram_on_cotree,
    matmul,
    rational_rank,
    spanning_tree,
)
from supplement.verify_independent import independent_certificate


class FiniteBlockCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.block = block_complex()

    def test_cellular_complex(self):
        self.assertEqual(len(self.block["vertices"]), 81)
        self.assertEqual(len(self.block["edges"]), 216)
        self.assertEqual(len(self.block["plaquettes"]), 216)
        self.assertTrue(all(x == 0 for row in matmul(self.block["d1"], self.block["d0"]) for x in row))

    def test_exact_ranks(self):
        self.assertEqual(rational_rank(self.block["d0"])[0], 80)
        self.assertEqual(rational_rank(self.block["d1"])[0], 136)

    def test_tree_gauge_and_retained_rank(self):
        tree = spanning_tree(self.block["vertices"], self.block["edges"])
        cotree = [i for i in range(216) if i not in set(tree)]
        retained = [[row[e] for e in cotree] for row in self.block["coarse"]]
        self.assertEqual((len(tree), len(cotree), rational_rank(retained)[0]), (80, 136, 17))

    def test_exact_coercivity_floor(self):
        tree = spanning_tree(self.block["vertices"], self.block["edges"])
        cotree = [i for i in range(216) if i not in set(tree)]
        result = exact_ldlt_floor(gram_on_cotree(self.block["d1"], cotree), Q(1, 25))
        self.assertTrue(result["positive"])

    def test_reverse_tree_hostile_case(self):
        tree = spanning_tree(self.block["vertices"], self.block["edges"], reverse=True)
        cotree = [i for i in range(216) if i not in set(tree)]
        result = exact_ldlt_floor(gram_on_cotree(self.block["d1"], cotree), Q(1, 25))
        self.assertTrue(result["positive"])

    def test_orientation_congruence(self):
        tree = spanning_tree(self.block["vertices"], self.block["edges"])
        cotree = [i for i in range(216) if i not in set(tree)]
        h = gram_on_cotree(self.block["d1"], cotree)
        signs = [(-1 if i % 2 else 1) for i in range(len(cotree))]
        oriented = [[signs[i] * h[i][j] * signs[j] for j in range(len(h))] for i in range(len(h))]
        self.assertTrue(exact_ldlt_floor(oriented, Q(1, 25))["positive"])

    def test_analytic_budget(self):
        result = analytic_budgets()
        self.assertTrue(result["all_checks_pass"])
        self.assertEqual(result["consequences"]["conditional_transport_ceiling"], "1/3")

    def test_hostile_radius_fails_closed(self):
        with self.assertRaises(ValueError):
            analytic_budgets(Q(1, 2), Q(1, 10**18))

    def test_hostile_time_fails_closed(self):
        with self.assertRaises(ValueError):
            analytic_budgets(Q(1, 100_000), Q(1, 10**12))

    def test_full_certificate(self):
        self.assertTrue(certificate()["all_checks_pass"])

    def test_independent_arithmetic_kernel(self):
        self.assertTrue(independent_certificate()["all_checks_pass"])


if __name__ == "__main__":
    unittest.main()
