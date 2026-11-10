import math
import unittest

import numpy as np

from su2_boundary_state_disintegration import (
    boundary_labels,
    gauge_transform,
    grid_2x2_block,
    omitted_boundary_edge_counterexample,
    perimeter_holonomy,
    plaquette_holonomy,
    qexp,
    qinv,
    qmul,
    random_su2,
    reflect_links,
    relative_tree_normalize,
)


class BoundaryDisintegrationTests(unittest.TestCase):
    def setUp(self):
        self.block = grid_2x2_block()
        self.rng = np.random.default_rng(20260720)
        self.links = np.asarray([random_su2(self.rng) for _ in self.block.edges])

    def test_block_counts(self):
        self.assertEqual(len(self.block.vertices), 9)
        self.assertEqual(len(self.block.edges), 12)
        self.assertEqual(len(self.block.plaquettes), 4)
        self.assertEqual(len(self.block.boundary), 8)
        self.assertEqual(len(self.block.retained_edges), 8)
        self.assertEqual(len(self.block.fiber_edges), 3)

    def test_quaternion_inverse(self):
        q = random_su2(self.rng)
        self.assertTrue(np.allclose(qmul(q, qinv(q)), [1, 0, 0, 0]))

    def test_forest_edge_is_fixed_to_identity(self):
        normalized, _, _ = relative_tree_normalize(self.block, self.links)
        forest_edge = next(iter(self.block.forest_parent.values()))[1]
        self.assertTrue(np.allclose(normalized[forest_edge], [1, 0, 0, 0]))

    def test_interior_gauge_invariance(self):
        center = (1, 1)
        gauge = {vertex: np.array([1.0, 0.0, 0.0, 0.0]) for vertex in self.block.vertices}
        gauge[center] = random_su2(self.rng)
        transformed = gauge_transform(self.block, self.links, gauge)
        normal_a, _, _ = relative_tree_normalize(self.block, self.links)
        normal_b, _, _ = relative_tree_normalize(self.block, transformed)
        self.assertTrue(np.allclose(normal_a, normal_b, atol=1e-12))

    def test_boundary_covariance(self):
        gauge = {vertex: random_su2(self.rng) for vertex in self.block.vertices}
        transformed = gauge_transform(self.block, self.links, gauge)
        normal_a, _, roots = relative_tree_normalize(self.block, self.links)
        normal_b, _, _ = relative_tree_normalize(self.block, transformed)
        for index, edge in enumerate(self.block.edges):
            expected = qmul(qmul(gauge[roots[edge.source]], normal_a[index]), qinv(gauge[roots[edge.target]]))
            self.assertTrue(np.allclose(normal_b[index], expected, atol=1e-11))

    def test_plaquette_holonomy_is_conjugated(self):
        gauge = {vertex: random_su2(self.rng) for vertex in self.block.vertices}
        transformed = gauge_transform(self.block, self.links, gauge)
        for index, plaquette in enumerate(self.block.plaquettes):
            base_vertex = self.block.edges[plaquette.oriented_edges[0][0]].source
            expected = qmul(qmul(gauge[base_vertex], plaquette_holonomy(self.block, self.links, index)), qinv(gauge[base_vertex]))
            self.assertTrue(np.allclose(plaquette_holonomy(self.block, transformed, index), expected, atol=1e-11))

    def test_perimeter_trace_is_gauge_invariant(self):
        gauge = {vertex: random_su2(self.rng) for vertex in self.block.vertices}
        transformed = gauge_transform(self.block, self.links, gauge)
        self.assertAlmostEqual(perimeter_holonomy(self.block, self.links)[0], perimeter_holonomy(self.block, transformed)[0])

    def test_reflection_commutes_with_normalization(self):
        left, _, _ = relative_tree_normalize(self.block, reflect_links(self.block, self.links))
        normal, _, _ = relative_tree_normalize(self.block, self.links)
        right = reflect_links(self.block, normal)
        self.assertTrue(np.allclose(left, right, atol=1e-11))

    def test_reflection_is_involution(self):
        self.assertTrue(np.allclose(reflect_links(self.block, reflect_links(self.block, self.links)), self.links))

    def test_labels_detect_identity_stabilizer(self):
        identity = np.tile([1.0, 0.0, 0.0, 0.0], (len(self.block.edges), 1))
        labels = boundary_labels(self.block, identity)
        self.assertEqual(labels.stabilizer_type, "central-SU2")
        self.assertEqual(labels.center_sign, 1)

    def test_labels_detect_negative_center_and_cut(self):
        links = np.tile([1.0, 0.0, 0.0, 0.0], (len(self.block.edges), 1)).astype(float)
        edge = self.block.retained_edges[0]
        links[edge] = qexp([math.pi, 0.0, 0.0])
        labels = boundary_labels(self.block, links, cut_tolerance=1e-8)
        self.assertEqual(labels.center_sign, -1)
        self.assertTrue(labels.near_cut_locus)

    def test_omitted_boundary_edge_changes_conditional_weight(self):
        result = omitted_boundary_edge_counterexample()
        self.assertTrue(result["conditional_weights_differ"])

    def test_bad_shape_rejected(self):
        with self.assertRaises(ValueError):
            relative_tree_normalize(self.block, np.zeros((3, 4)))

    def test_all_vertices_have_roots(self):
        _, _, roots = relative_tree_normalize(self.block, self.links)
        self.assertEqual(set(roots), set(self.block.vertices))


if __name__ == "__main__":
    unittest.main()

