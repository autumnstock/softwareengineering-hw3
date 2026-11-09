import math
import unittest
from unittest.mock import patch
import global_game_data
import graph_data
import pathing



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

    def tearDown(self):
        """Restores original graph data after running tests"""
        global_game_data.current_graph_index = self.orig_graph_index
        graph_data.graph_data = self.orig_graph_data

    def test_bfs_path_validity(self):
        """Tests that BFS finds a valid path from start to target to exit"""
        path = pathing.get_bfs_path()
        self.assertIn(global_game_data.target_node, path)
        self.assertEqual(path[-1], global_game_data.exit_node)

        graph = graph_data.graph_data[global_game_data.current_graph_index]
        for u, v in zip(path[:-1], path[1:]):
            self.assertIn(v, graph.get(u, []), f"No edge between {u} and {v}")

    def test_bfs_shortest_path(self):
        """Tests that BFS returns optimal shortest path"""
        path = pathing.get_bfs_path()
        expected_path = [0, 1, 2, 3]
        self.assertEqual(path, expected_path)

    def test_dfs_path_validity(self):
        """Tests that DFS finds a valid path from start to target to exit."""
        path = pathing.get_dfs_path()


        self.assertIn(global_game_data.target_node, path)
        self.assertEqual(path[-1], global_game_data.exit_node)


        graph = graph_data.graph_data[global_game_data.current_graph_index]
        for u, v in zip(path[:-1], path[1:]):
            self.assertIn(v, graph.get(u, []), f"No edge between {u} and {v}")

    def test_dfs_neighbor_order(self):
        """
        Tests that DFS prpoduces the expected path based on neighbor order sorting
        """
        path = pathing.get_dfs_path()
        self.assertEqual(path[0], global_game_data.start_node)
        self.assertIn(global_game_data.target_node, path)
        self.assertEqual(path[-1], global_game_data.exit_node)

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

    def test_extra_graph_edges_are_bidirectional(self):
        extra_graph = self.orig_graph_data[-1]

        for node, node_data in enumerate(extra_graph):
            for neighbor in node_data[1]:
                self.assertIn(
                    node,
                    extra_graph[neighbor][1],
                    f"Edge {node} -> {neighbor} is not bidirectional"
                )

    def test_dijkstra_path_validity(self):
        """Dijkstra must travel Start to Target to Exit"""
        with patch.object(pathing, "_edge_distance", return_value=1):
            path = pathing.get_dijkstra_path()

        self.assertEqual(path[0], global_game_data.start_node)
        self.assertIn(global_game_data.target_node, path)
        self.assertEqual(path[-1], global_game_data.exit_node)

        graph = graph_data.graph_data[
            global_game_data.current_graph_index
        ]

        for u, v in zip(path[:-1], path[1:]):
            self.assertIn(
                v, graph.get(u, []),
                f"No edge between {u} and {v}"
            )

    def test_dijkstra_shortest_weighted_path(self):
        """Dijkstra must minimize distance, not edge count."""
        weights = {
            (0, 1): 10,
            (0, 4): 1,
            (4, 5): 1,
            (5, 2): 1,
            (1, 2): 10,
            (2, 3): 1
        }

        def mock_distance(u, v):
            return weights.get(
                (u, v),
                weights.get((v, u))
            )

        with patch.object(
            pathing, "_edge_distance", side_effect=mock_distance
        ):
            result = pathing.get_dijkstra_path()

        # Shortest weighted route:
        # 0 -> 4 -> 5 -> 2 -> 3
        # Total cost = 1 + 1 + 1 + 1 = 4
        self.assertEqual(result, [0, 4, 5, 2, 3])

    def test_dijkstra_priority_update(self):
        """A shorter discovered route must update the priority."""
        graph = {
            0: [1, 4],
            1: [0, 2],
            2: [1, 3, 5],
            3: [2],
            4: [0, 5],
            5: [2, 4]
        }

        weights = {
            (0, 1): 10,
            (0, 4): 1,
            (4, 5): 1,
            (5, 2): 1,
            (1, 2): 1,
            (2, 3): 1
        }

        def mock_distance(u, v):
            return weights.get(
                (u, v),
                weights.get((v, u))
            )

        with patch.object(
            pathing, "_edge_distance", side_effect=mock_distance
        ):
            result = pathing._dijkstra_segment(graph, 0, 1)

        self.assertEqual(result, [0, 4, 5, 2, 1])

    def test_dijkstra_start_equals_goal(self):
        """Dijkstra should return one node when start equals goal."""
        graph = {0: [1], 1: [0]}

        with patch.object(pathing, "_edge_distance", return_value=1):
            result = pathing._dijkstra_segment(graph, 0, 0)

        self.assertEqual(result, [0])

    def test_dijkstra_unreachable_goal(self):
        """Dijkstra should return [] when no path exists."""
        graph = {
            0: [1],
            1: [0],
            2: []
        }

        with patch.object(pathing, "_edge_distance", return_value=1):
            result = pathing._dijkstra_segment(graph, 0, 2)

        self.assertEqual(result, [])

    def test_a_star_path_validity(self):
        """A* must start at Start, visit Target, and end at Exit."""
        from unittest.mock import patch

        with patch.object(pathing, "_edge_distance", return_value=1):
            path = pathing.get_a_star_path()

        self.assertEqual(path[0], global_game_data.start_node)
        self.assertIn(global_game_data.target_node, path)
        self.assertEqual(path[-1], global_game_data.exit_node)

        graph = graph_data.graph_data[
            global_game_data.current_graph_index
        ]

        for u, v in zip(path[:-1], path[1:]):
            self.assertIn(v, graph[u])

    def test_a_star_shortest_path(self):
        """A* should find a shortest path with unit edge costs."""
        from unittest.mock import patch

        with patch.object(pathing, "_edge_distance", return_value=1):
            path = pathing.get_a_star_path()

        self.assertEqual(path, [0, 1, 2, 3])

    def test_a_star_unreachable(self):
        """A* should return an empty path if goal is unreachable."""
        from unittest.mock import patch

        graph = {
            0: [1],
            1: [0],
            2: []
        }

        with patch.object(pathing, "_edge_distance", return_value=1):
            path = pathing._a_star_segment(graph, 0, 2)

        self.assertEqual(path, [])

    def test_edge_distance(self):
        """Verify Euclidean edge distance calculation."""
        graph_data.graph_data = [[
            [(0, 0), [1]],
            [(3, 4), [0]]
        ]]

        global_game_data.current_graph_index = 0
        distance = pathing._edge_distance(0, 1)
        self.assertAlmostEqual(distance, 5.0)


    


if __name__ == '__main__':
    unittest.main()
