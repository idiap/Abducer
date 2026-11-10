import unittest
from history_uniform_dispersion_comparison import *


class Tests(unittest.TestCase):
    def row(self,a=False,b=False): return HistoryRow(.001,.001,0,.001,a,b)
    def test_complete_table(self):
        c=history_comparison_certificate({():self.row()},[()],.01); self.assertTrue(c.numerical_table_closes)
    def test_incomplete_rejected(self):
        with self.assertRaises(ValueError): history_comparison_certificate({},[()],.1)
    def test_extra_rejected(self):
        with self.assertRaises(ValueError): history_comparison_certificate({():self.row(),(0,):self.row()},[()],.1)
    def test_zero_mass_rejected(self):
        with self.assertRaises(ValueError): history_comparison_certificate({():HistoryRow(0,0,0,0,True,True,False)},[()],.1)
    def test_premises_close_physical(self):
        c=history_comparison_certificate({():self.row(True,True)},[()],.01); self.assertTrue(c.physical_history_uniform_bound_proved)
    def test_missing_premise_blocks(self):
        c=history_comparison_certificate({():self.row(True,False)},[()],.01); self.assertFalse(c.physical_history_uniform_bound_proved)
    def test_restricted_numerical_closes(self): self.assertTrue(calibration()["history_certificate"]["numerical_table_closes"])
    def test_physical_open(self): self.assertFalse(calibration()["physical_positive_mass_history_table_proved"])
    def test_adaptive_available(self): self.assertTrue(calibration()["history_certificate"]["adaptive_domination_implication_available"])
    def test_restricted_adaptive(self): self.assertTrue(calibration()["restricted_adaptive_certificate"]["strict_cluster_subcritical"])
    def test_schema_fields(self): self.assertEqual(len(calibration()["retained_schema_additions"]),3)
    def test_total_formula(self): self.assertAlmostEqual(self.row().total_upper(),.003)
    def test_invalid_negative(self):
        with self.assertRaises(ValueError): history_comparison_certificate({():HistoryRow(-1,0,0,0,True,True)},[()],.1)
    def test_target_respected(self):
        c=calibration()["history_certificate"]; self.assertLess(c["numerical_maximum_row"],c["target_continuous_budget"])


if __name__ == "__main__": unittest.main()
