import unittest
from permutation import SJTGraphSolver

class TestSJTandHamiltonian(unittest.TestCase):

    def test_sjt_permutation_count(self):
        dummy_graph = {0: [1, 2], 1: [2, 3], 2: [3, 0], 3: [0]}
        solver = SJTGraphSolver(dummy_graph)
        
        perms = list(solver.generate_permutations([1, 2, 3]))
        self.assertEqual(len(perms), 6)

    def test_sjt_unique_permutations(self):
        dummy_graph = {0: [1, 2], 1: [2, 3], 2: [3, 0], 3: [0]}
        solver = SJTGraphSolver(dummy_graph)
        
        perms = list(solver.generate_permutations([1, 2, 3]))
        unique_perms = set(tuple(p) for p in perms)
        self.assertEqual(len(unique_perms), 6)

    def test_hamiltonian_detection(self):
        graph = {
            0: [1],
            1: [2],
            2: [3],
            3: [0]
        }
        solver = SJTGraphSolver(graph)
        valid_cycles = solver.find_all_cycles()
        
        self.assertNotEqual(valid_cycles, -1)
        self.assertIn([0, 1, 2, 3, 0], valid_cycles)
    
    def test_no_valid_hamiltonian_cycle(self):
        graph = {
            0: [1],
            1: [],
            2: [3],
            3: [0]
        }
        solver = SJTGraphSolver(graph)
        result = solver.find_all_cycles()
        self.assertEqual(result, -1)

if __name__ == '__mainn__':
    unittest.main()