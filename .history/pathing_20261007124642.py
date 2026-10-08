import graph_data
import global_game_data
from numpy import random

def set_current_graph_paths():
    global_game_data.graph_paths.clear()
    global_game_data.graph_paths.append(get_test_path())
    global_game_data.graph_paths.append(get_random_path())
    global_game_data.graph_paths.append(get_dfs_path())
    global_game_data.graph_paths.append(get_bfs_path())
    global_game_data.graph_paths.append(get_dijkstra_path())


def get_test_path():
    return graph_data.test_path[global_game_data.current_graph_index]

def assert_path_postconditions(graph, path, target_node, exit_node):
    """Validates postconditions for 5b and 7."""
    # Postcondition 7a: result path includes target node
    assert target_node in path, f"Path {path} does not contain target node {target_node}"
    # Postcondition 7b: result path ends at exit node
    assert len(path) > 0 and path[-1] == exit_node, f"Path {path} does not end at exit node {exit_node}"
    # Postcondition 7c: every pair of sequential vertices in path are connected by an edge
    for u, v in zip(path[:-1], path[1:]):
        assert v in graph.get(u, []), f"No edge between sequential nodes {u} and {v}"



def get_random_path():
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    start = global_game_data.start_node
    target = global_game_data.target_node
    exit_node = global_game_data.exit_node

    #Preconditions 5b
    assert start in graph, "Start node must be in graph"
    assert target in graph, "Target node must be in graph"
    assert exit_node in graph, "Exit node must be in graph"

    def random_walk(start_pt, end_pt, max_steps=1000):
        current = start_pt
        segment = [current]
        steps = 0
        while current != end_pt and steps < max_steps:
            neighbors = graph.get(current, [])
            if not neighbors:
                break
            current = random.choice(neighbors)
            segment.append(current)
            steps += 1
        return segment

        path1 = random_walk(start, target)
        path2 = random_walk(target, exit)

        full_path = path1 + path2[1:]

        assert_path_postconditions(graph, full_path, target, exit_node)
        return full_path


def get_dfs_path():
    return [1,2]


def get_bfs_path():
    return [1,2]


def get_dijkstra_path():
    return [1,2]
