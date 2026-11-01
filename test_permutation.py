import math
import unittest

from permutation import (
    SJTGraphSolver,
    generate_permutations,
    powerset,
)


def _is_adjacent_transposition(left, right):
    diffs = [i for i in range(len(left)) if left[i] != right[i]]
    if len(diffs) != 2:
        return False
    i, j = diffs
    return j == i + 1 and left[i] == right[j] and left[j] == right[i]


class TestSJT(unittest.TestCase):
    def test_permutation_counts(self):
        self.assertEqual(list(generate_permutations([])), [[]])
        self.assertEqual(list(generate_permutations([7])), [[7]])
        for n in range(2, 6):
            perms = list(generate_permutations(list(range(1, n + 1))))
            self.assertEqual(len(perms), math.factorial(n))

    def test_unique_and_complete(self):
        elements = [1, 2, 3, 4]
        perms = [tuple(p) for p in generate_permutations(elements)]
        self.assertEqual(len(set(perms)), math.factorial(4))
        self.assertEqual(perms[0], (1, 2, 3, 4))
        for perm in perms:
            self.assertEqual(sorted(perm), elements)

    def test_adjacent_transpositions(self):
        perms = list(generate_permutations([1, 2, 3, 4]))
        for previous, current in zip(perms, perms[1:]):
            self.assertTrue(_is_adjacent_transposition(previous, current), (previous, current))

    def test_method_matches_module_function(self):
        solver = SJTGraphSolver({0: [1], 1: [0, 2], 2: [1]})
        self.assertEqual(
            list(solver.generate_permutations([1, 2, 3])),
            list(generate_permutations([1, 2, 3])),
        )


class TestHamiltonianCycles(unittest.TestCase):
    def test_triangle_on_intermediate_nodes(self):
        graph = [
            [(0, 0), [1]],
            [(1, 0), [0, 2, 3]],
            [(1, 1), [1, 3]],
            [(2, 0), [1, 2, 4]],
            [(3, 0), [3]],
        ]
        solver = SJTGraphSolver(graph)
        cycles = solver.find_all_cycles()
        self.assertNotEqual(cycles, -1)
        self.assertIn([1, 2, 3, 1], cycles)
        self.assertIn([1, 3, 2, 1], cycles)
        for cycle in cycles:
            self.assertEqual(cycle[0], cycle[-1])
            self.assertNotIn(0, cycle)
            self.assertNotIn(4, cycle)

    def test_no_cycle_returns_minus_one(self):
        graph = {
            0: [1],
            1: [0, 2],
            2: [1, 3],
            3: [2, 4],
            4: [3],
        }
        solver = SJTGraphSolver(graph)
        self.assertEqual(solver.find_all_cycles(), -1)

    def test_too_few_intermediate_nodes(self):
        two_nodes = {0: [1], 1: [0]}
        three_nodes = {0: [1], 1: [0, 2], 2: [1]}
        self.assertEqual(SJTGraphSolver(two_nodes).find_all_cycles(), -1)
        self.assertEqual(SJTGraphSolver(three_nodes).find_all_cycles(), -1)

    def test_invalid_permutation_rejected(self):
        graph = {
            0: [1],
            1: [0, 2, 3],
            2: [1, 3],
            3: [1, 2, 4],
            4: [3],
        }
        solver = SJTGraphSolver(graph)
        self.assertTrue(solver.is_valid_hamiltonian_cycle([1, 2, 3]))
        self.assertFalse(solver.is_valid_hamiltonian_cycle([1, 2]))
        self.assertFalse(solver.is_valid_hamiltonian_cycle([1, 2, 3, 4]))

    def test_graph_data_small_debug_graph(self):
        import graph_data

        solver = SJTGraphSolver(graph_data.graph_data[6])
        cycles = solver.find_all_cycles()
        self.assertNotEqual(cycles, -1)
        self.assertTrue(any(cycle[:3] == [1, 2, 3] or cycle[:3] == [1, 3, 2] for cycle in cycles))


class TestOptimalCycles(unittest.TestCase):
    def test_euclidean_distance_and_ties(self):
        graph = [
            [(0, 0), [1]],
            [(0, 0), [0, 2, 3]],
            [(3, 0), [1, 3]],
            [(0, 4), [1, 2, 4]],
            [(10, 0), [3]],
        ]
        solver = SJTGraphSolver(graph)
        optimal, distance = solver.find_optimal_cycles()
        self.assertNotEqual(optimal, -1)
        expected = 3 + 5 + 4
        self.assertAlmostEqual(distance, expected)
        self.assertTrue(all(solver.cycle_distance(cycle) == distance for cycle in optimal))

    def test_weighted_dict_graph(self):
        graph = {
            0: {1: 1},
            1: {0: 1, 2: 1, 3: 10},
            2: {1: 1, 3: 1},
            3: {1: 10, 2: 1, 4: 1},
            4: {3: 1},
        }
        solver = SJTGraphSolver(graph)
        optimal, distance = solver.find_optimal_cycles()
        self.assertEqual(distance, 12)
        self.assertIn([1, 2, 3, 1], optimal)

    def test_optimal_without_cycles(self):
        graph = {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
        cycles, distance = SJTGraphSolver(graph).find_optimal_cycles()
        self.assertEqual(cycles, -1)
        self.assertEqual(distance, -1)


class TestLargestClique(unittest.TestCase):
    def test_powerset_size_and_no_itertools(self):
        nodes = [1, 2, 3]
        subsets = powerset(nodes)
        self.assertEqual(len(subsets), 8)
        self.assertIn([], subsets)
        self.assertIn([1, 2, 3], subsets)

    def test_triangle_is_largest(self):
        graph = {
            0: [1],
            1: [0, 2, 3],
            2: [1, 3],
            3: [1, 2, 4],
            4: [3],
        }
        clique, size = SJTGraphSolver(graph).find_largest_clique()
        self.assertEqual(size, 3)
        self.assertEqual(sorted(clique), [1, 2, 3])
        self.assertNotIn(0, clique)
        self.assertNotIn(4, clique)

    def test_no_edges_among_intermediates(self):
        graph = {0: [1, 2], 1: [0], 2: [0, 3], 3: [2]}
        clique, size = SJTGraphSolver(graph).find_largest_clique()
        self.assertEqual(size, 1)
        self.assertEqual(len(clique), 1)


if __name__ == "__main__":
    unittest.main()
