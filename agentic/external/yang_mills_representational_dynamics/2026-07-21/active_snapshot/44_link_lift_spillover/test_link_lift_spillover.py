import unittest
import numpy as np
from link_lift_spillover import *


class Tests(unittest.TestCase):
    def test_basis_shape(self): self.assertEqual(centered_basis(6).shape,(6,5))
    def test_basis_orthonormal(self):
        q=centered_basis(6); self.assertLess(np.linalg.norm(q.T@q-np.eye(5)),1e-12)
    def test_basis_centered(self): self.assertLess(np.linalg.norm(np.ones(6)@centered_basis(6)),1e-12)
    def test_invalid_basis(self):
        with self.assertRaises(ValueError): centered_basis(1)
    def test_eight_links(self): self.assertEqual(spillover_certificate().interior_links,8)
    def test_rank_five(self): self.assertEqual(spillover_certificate().centered_constraint_rank,5)
    def test_one_zero_mode(self): self.assertEqual(spillover_certificate().zero_spill_modes,1)
    def test_four_positive_modes(self): self.assertEqual(sum(x>1e-10 for x in spillover_certificate().minimum_spill_eigenvalues),4)
    def test_spectra_equal(self): self.assertTrue(spillover_certificate().spectra_equal_for_all_interior_links)
    def test_external_minimum(self): self.assertTrue(spillover_certificate().exact_external_minimization)
    def test_actual_exceeds_admissible(self):
        c=calibration()["repair_accounting"]; self.assertGreater(c["actual_to_admissible_ratio"],1)
    def test_repair_fails(self): self.assertFalse(calibration()["repair_accounting"]["single_star_link_lift_closes"])
    def test_falsification(self): self.assertTrue(calibration()["generic_single_star_repair_falsified"])
    def test_polymer_open(self): self.assertFalse(calibration()["coordinated_polymer_repair_proved"])
    def test_invalid_free_energy(self):
        with self.assertRaises(ValueError): lifted_free_energy(-1,1,.5,1,1,1,1)


if __name__ == "__main__": unittest.main()
