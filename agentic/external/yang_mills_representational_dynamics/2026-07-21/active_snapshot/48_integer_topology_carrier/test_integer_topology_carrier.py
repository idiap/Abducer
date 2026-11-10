import unittest
import numpy as np
from integer_topology_carrier import *


class Tests(unittest.TestCase):
    def test_zero(self): self.assertEqual(pfaffian_charge([0]*6),0)
    def test_basic_charge(self): self.assertEqual(pfaffian_charge([1,0,0,0,0,1]),1)
    def test_sign(self): self.assertEqual(pfaffian_charge([0,1,0,0,1,0]),-1)
    def test_center_reduction(self): self.assertEqual(center_reduction([2,-1,0,0,0,0]),(0,1,0,0,0,0))
    def test_invalid_flux_length(self):
        with self.assertRaises(ValueError): validate_fluxes([1]*5)
    def test_invalid_noninteger(self):
        with self.assertRaises(ValueError): validate_fluxes([0,0,0,0,0,.5])
    def test_pfaffian_determinant(self):
        f=(2,-1,3,1,0,2); self.assertAlmostEqual(np.linalg.det(antisymmetric_flux_matrix(f)),pfaffian_charge(f)**2)
    def test_same_center_different_charge(self): self.assertTrue(calibration()["same_center_labels_different_integer_charge"])
    def test_unbounded_family_center(self): self.assertEqual(erased_center_family(7).center_reduction,(0,)*6)
    def test_unbounded_family_charge(self): self.assertEqual(erased_center_family(7).pfaffian_charge,196)
    def test_negative_scale(self):
        with self.assertRaises(ValueError): erased_center_family(-1)
    def test_catalog_has_64_labels(self): self.assertEqual(calibration()["bounded_catalog"]["center_labels_observed"],64)
    def test_integer_schema_required(self): self.assertTrue(calibration()["retained_schema_requires_integer_flux_lift"])
    def test_nonabelian_open(self): self.assertFalse(calibration()["complete_nonabelian_su2_second_chern_control_proved"])
    def test_sector_weight_open(self): self.assertFalse(calibration()["sector_weight_bound_proved"])


if __name__ == "__main__": unittest.main()
