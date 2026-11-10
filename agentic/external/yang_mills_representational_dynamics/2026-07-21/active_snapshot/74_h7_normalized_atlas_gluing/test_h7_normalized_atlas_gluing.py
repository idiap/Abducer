import json
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

import h7_normalized_atlas_gluing as h7


class AtlasGeometryTests(unittest.TestCase):
    def test_two_center_cover_and_multiplicity(self):
        self.assertTrue(h7.check_cover())
        self.assertEqual(max(h7.multiplicity(x) for x in h7.ATOMS), 2)
        self.assertNotIn("minus_pole", h7.SUPPORT[h7.PLUS])
        self.assertNotIn("plus_pole", h7.SUPPORT[h7.MINUS])

    def test_subordinate_positive_partition(self):
        for atom in h7.ATOMS:
            self.assertEqual(h7.partition_sum(atom), 1)
            for chart in h7.CHARTS:
                weight = h7.PARTITION[chart][atom]
                self.assertEqual(weight > 0, atom in h7.SUPPORT[chart])

    def test_overlap_reconstruction_exact(self):
        for atom in h7.OVERLAP:
            self.assertNotEqual(
                h7.CHART_COORDINATES[h7.PLUS][atom],
                h7.CHART_COORDINATES[h7.MINUS][atom],
            )
            self.assertEqual(
                h7.reconstruct_overlap_coordinate(atom, h7.PLUS),
                h7.reconstruct_overlap_coordinate(atom, h7.MINUS),
            )
            self.assertEqual(
                h7.reconstruct_overlap_coordinate(atom, h7.PLUS),
                h7.QUATERNIONS[atom],
            )

    def test_perturbed_minus_chart_coordinate_fails_reconstruction(self):
        for atom in h7.OVERLAP:
            hostile = h7.reconstruct_overlap_coordinate(
                atom,
                h7.MINUS,
                coordinate_override=h7.CHART_COORDINATES[h7.PLUS][atom],
            )
            self.assertNotEqual(hostile, h7.QUATERNIONS[atom])


class NormalizedGluingTests(unittest.TestCase):
    def setUp(self):
        self.mu = h7.regular_history()

    def test_probability_and_chart_conditionals_normalized(self):
        self.assertEqual(sum(self.mu.values()), 1)
        self.assertEqual(
            sum(h7.chart_mass(self.mu, chart) for chart in h7.CHARTS), 1
        )
        for chart in h7.CHARTS:
            conditional = h7.chart_conditional(self.mu, chart)
            self.assertEqual(sum(conditional.values()), 1)
            self.assertGreater(h7.chart_mass(self.mu, chart), 0)

    def test_exact_global_gluing_for_all_64_events(self):
        events = list(h7.all_events())
        self.assertEqual(len(events), 64)
        for event in events:
            self.assertEqual(
                h7.glued_event_mass(self.mu, event), h7.event_mass(self.mu, event)
            )

    def test_exceptional_channel_gluing_for_all_events(self):
        decomposition = h7.exceptional_decomposition(self.mu)
        self.assertEqual(
            sum(decomposition.regular_chart_coefficients.values())
            + decomposition.exceptional_coefficient,
            1,
        )
        self.assertEqual(decomposition.exceptional_coefficient, Fraction(2, 25))
        for event in h7.all_events():
            self.assertEqual(
                h7.exceptional_glued_event_mass(self.mu, event),
                h7.event_mass(self.mu, event),
            )

    def test_full_overlap_transition_identity(self):
        for atom in h7.OVERLAP:
            self.assertEqual(
                h7.transition_residual(self.mu, h7.PLUS, h7.MINUS, atom), 0
            )
            self.assertEqual(
                h7.transition_residual(self.mu, h7.MINUS, h7.PLUS, atom), 0
            )

    def test_jacobian_and_transition_cocycles(self):
        self.assertEqual(
            h7.jacobian(h7.PLUS, h7.MINUS, "equator_x"), Fraction(3, 2)
        )
        self.assertEqual(
            h7.jacobian(h7.PLUS, h7.MINUS, "equator_y"), Fraction(2, 5)
        )
        for atom in h7.OVERLAP:
            self.assertEqual(
                h7.jacobian(h7.PLUS, h7.MINUS, atom)
                * h7.jacobian(h7.MINUS, h7.PLUS, atom),
                1,
            )
            self.assertEqual(
                h7.transition_factor(self.mu, h7.PLUS, h7.MINUS, atom)
                * h7.transition_factor(self.mu, h7.MINUS, h7.PLUS, atom),
                1,
            )

    def test_two_block_shared_edge_consistency(self):
        certificate = h7.two_block_overlap_certificate(self.mu)
        self.assertTrue(certificate["all_shared_coordinates_exact"])
        self.assertTrue(certificate["all_cocycles_exact"])
        self.assertEqual(len(certificate["records"]), 2)

    def test_invalid_history_rejected(self):
        invalid = h7.regular_history()
        invalid["plus_pole"] = Fraction(0)
        with self.assertRaises(ValueError):
            h7.chart_mass(invalid, h7.PLUS)


class HostileHistoryTests(unittest.TestCase):
    def test_arbitrarily_small_chart_mass(self):
        previous = Fraction(1)
        for n in (4, 16, 256, 65536):
            mu = h7.hostile_chart_history(n)
            mass = h7.chart_mass(mu, h7.PLUS)
            self.assertEqual(mass, Fraction(3, 4 * n))
            self.assertLess(mass, previous)
            previous = mass

    def test_unnormalized_numerator_failure(self):
        for n in (4, 16, 256, 65536):
            mu = h7.hostile_chart_history(n)
            numerator = mu["plus_pole"] * h7.PARTITION[h7.PLUS]["plus_pole"]
            normalized = h7.chart_conditional(mu, h7.PLUS)["plus_pole"]
            self.assertEqual(numerator, Fraction(1, 4 * n))
            self.assertEqual(normalized, Fraction(1, 3))
            self.assertEqual(normalized / numerator, Fraction(4 * n, 3))

    def test_coverage_is_not_exceptional_probability_control(self):
        self.assertTrue(h7.check_cover())
        previous = Fraction(0)
        for n in (4, 16, 256, 65536):
            mu = h7.hostile_exception_history(n)
            epsilon = h7.event_mass(mu, h7.EXCEPTIONAL)
            self.assertEqual(epsilon, 1 - Fraction(1, n))
            self.assertGreater(epsilon, previous)
            previous = epsilon


class OutputGuardrailTests(unittest.TestCase):
    def test_calibration_guardrails(self):
        results = h7.calibration()
        self.assertEqual(results["claim_level"], "C2 finite atlas theorem")
        guardrails = results["guardrails"]
        self.assertFalse(guardrails["physical_boundary_uniform_SU2_kernel_proved"])
        self.assertFalse(guardrails["history_uniform_exceptional_bound_proved"])
        self.assertFalse(guardrails["RG_iteration_proved"])
        self.assertFalse(guardrails["continuum_or_mass_gap_proved"])

    def test_json_output_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "results.json"
            h7.write_results(path)
            loaded = json.loads(path.read_text())
            self.assertEqual(loaded, h7.calibration())


if __name__ == "__main__":
    unittest.main()
