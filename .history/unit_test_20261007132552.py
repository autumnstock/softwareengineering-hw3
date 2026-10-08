import math
import unittest
import global_game_data
import graph_data


class TestPathFinding(unittest.TestCase):

    def setUp(self):
        """
        Sets up a mock graph structure for testing:
        
            (0) --- (1) --- (2) --- (3)
             |               |
            (4) ------------ (5)
        
        Adjacency representation:
        0: [1, 4]
        1: [0, 2]
        2: [1, 3, 5]
        3: [2]
        4: [0, 5]
        5: [2, 4]
        """
        self.orig_graph_index = global_game_data.current_graph_index
        self.orig_graph_data = graph_data.graph_data

        global_game_data.current_graph_index = 0

        mock_adj_graph = {
            0: [1, 4],
            1: [0, 2],
            2: [1, 3, 5],
            3: [2],
            4: [0, 5],
            5: [2, 4]
        }

        graph_data.graph_data = [mock_adj_graph]

        global_game_data.start_node = 0
        global_game_data.target_node = 2
        global_game_data.exit_node = 3



    def test_upper(self):
        self.assertEqual('test'.upper(), 'TEST')

    def test_isupper(self):
        self.assertTrue('TEST'.isupper())
        self.assertFalse('Test'.isupper())

    def test_floating_point_estimation(self):
        first_value = 0
        for x in range(1000):
            first_value += 1/100
        second_value = 10
        almost_pi = 3.1
        pi = math.pi
        self.assertNotEqual(first_value,second_value)
        self.assertAlmostEqual(first=first_value,second=second_value,delta=1e-9)
        self.assertNotEqual(almost_pi, pi)
        self.assertAlmostEqual(first=almost_pi, second=pi, delta=1e-1)


if __name__ == '__main__':
    unittest.main()
