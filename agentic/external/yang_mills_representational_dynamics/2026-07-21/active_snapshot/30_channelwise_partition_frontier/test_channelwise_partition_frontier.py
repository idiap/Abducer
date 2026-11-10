import unittest

from channelwise_partition_frontier import (
    calibration,
    channel_ledger,
    frontier_certificate,
    remedy_frontier,
)


class ChannelwiseFrontierTests(unittest.TestCase):
    def test_five_channels(self):
        self.assertEqual(len(channel_ledger()), 5)

    def test_channel_names_unique(self):
        names = [c.channel for c in channel_ledger()]
        self.assertEqual(len(names), len(set(names)))

    def test_center_not_promoted(self):
        center = channel_ledger()[0]
        self.assertIn("restricted_exact", center.status)
        self.assertFalse(center.physical_su2_channel_closed)

    def test_coherent_conditional_progress(self):
        coherent = channel_ledger()[1]
        self.assertIn("closed conditional", coherent.status)
        self.assertTrue(coherent.normalized_partition_bound)
        self.assertFalse(coherent.boundary_state_uniform)

    def test_incoherent_gap_is_negative(self):
        incoherent = channel_ledger()[2]
        self.assertLess(incoherent.numerical_bound, 0.0)

    def test_topology_unrepresented(self):
        topology = channel_ledger()[-1]
        self.assertIn("unrepresented", topology.status)
        self.assertIsNone(topology.numerical_bound)

    def test_no_physical_channel_closed(self):
        self.assertEqual(frontier_certificate().physically_closed_channel_count, 0)

    def test_claim_ceiling(self):
        cert = frontier_certificate()
        self.assertFalse(cert.physical_partition_ratio_proved)
        self.assertFalse(cert.one_scale_basin_entry_proved)
        self.assertFalse(cert.mass_gap_proved)

    def test_remedy_frontier_monotone(self):
        points = remedy_frontier()
        degrees = [p.maximum_effective_degree_for_required_free_energy for p in points]
        self.assertTrue(all(d is not None for d in degrees))
        self.assertTrue(all(degrees[j + 1] > degrees[j] for j in range(len(degrees) - 1)))

    def test_unit_charge_requires_degree_reduction(self):
        first = remedy_frontier()[0]
        self.assertLess(first.maximum_effective_degree_for_required_free_energy, 18)
        self.assertFalse(first.current_degree_admissible)

    def test_terminal_amplification_admits_current_degree(self):
        last = remedy_frontier()[-1]
        self.assertTrue(last.current_degree_admissible)

    def test_frontier_free_energy_matches_stage26(self):
        self.assertAlmostEqual(frontier_certificate().required_uniform_free_energy, 6.712921011389365)

    def test_calibration_ranked_targets(self):
        data = calibration()
        self.assertEqual(len(data["ranked_next_targets"]), 5)

    def test_calibration_stop(self):
        data = calibration()
        self.assertIn("no physical channel", data["epistemic_stop"])

    def test_every_channel_has_open_requirement(self):
        self.assertTrue(all(c.first_open_requirement for c in channel_ledger()))


if __name__ == "__main__":
    unittest.main()
