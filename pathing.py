import graph_data
import global_game_data
import random
import heapq
from collections import deque


def _adjacency_graph(raw_graph):
    """Convert game graph list format to node -> neighbors adjacency dict."""
    if isinstance(raw_graph, dict):
        return raw_graph
    return {index: raw_graph[index][1] for index in range(len(raw_graph))}


def _sync_graph_nodes():
    """Start and exit indices for the current graph (see graph_data.py)."""
    raw = graph_data.graph_data[global_game_data.current_graph_index]
    global_game_data.start_node = 0
    global_game_data.exit_node = len(raw) - 1


def _current_adjacency_graph():
    return _adjacency_graph(graph_data.graph_data[global_game_data.current_graph_index])


def set_current_graph_paths():
    _sync_graph_nodes()
    global_game_data.graph_paths.clear()
    global_game_data.graph_paths.append(get_test_path())
    global_game_data.graph_paths.append(get_random_path())
    global_game_data.graph_paths.append(get_dfs_path())
    global_game_data.graph_paths.append(get_bfs_path())
    


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
    graph = _current_adjacency_graph()
    start = global_game_data.start_node
    target = global_game_data.target_node
    exit_node = global_game_data.exit_node

    #Preconditions 5b
    assert start in graph, "Start node must be in graph"
    assert target in graph, "Target node must be in graph"
    assert exit_node in graph, "Exit node must be in graph"

    def random_walk(start_pt, end_pt):
        current = start_pt
        segment = [current]
        visited = {current}
        while current != end_pt:
            neighbors = [
                node for node in graph[current]
                if node not in visited
            ]

            if neighbors:
                next_node = random.choice(neighbors)
                segment.append(next_node)
                visited.add(next_node)
                current = next_node
            else:
                if len(segment) == 1:
                    raise ValueError("No path to destination")
                
                segment.pop()
                current = segment[-1]
        
        return segment

    path1 = random_walk(start, target)
    path2 = random_walk(target, exit_node)
    full_path = path1 + path2[1:]

    assert full_path[0] == start, "Path must begin at start"
    assert path1[-1] == target, "First segment must reach target"
    assert path2[-1] == exit_node, "Second segment must reach exit"

    assert_path_postconditions(graph, full_path, target, exit_node)
    return full_path

def _dfs_segment(graph, start, goal):
    """Helper to perform iterative DFS from start to goal."""
    stack = [[start]]

    while stack:
        path = stack.pop()
        node = path[-1]

        if node == goal:
            return path

        neighbors = sorted(graph.get(node, []), reverse=True)
        for neighbor in neighbors:
            if neighbor not in path:
                stack.append(path + [neighbor])
    return []

def get_dfs_path():
    graph = _current_adjacency_graph()
    start = global_game_data.start_node
    target = global_game_data.target_node
    exit_node = global_game_data.exit_node

    segment1 = _dfs_segment(graph, start,target)
    segment2 = _dfs_segment(graph, target, exit_node)

    full_path = segment1 + segment2[1:]

    assert segment1, "No path from start to target"
    assert segment2, "No path from target to exit"
    assert full_path[0] == start

    assert_path_postconditions(graph, full_path, target, exit_node)
    return full_path




def _bfs_segment(graph, start, goal):
    """Helper to perform BFS from start to goal"""
    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        for neighbor in sorted(graph.get(node, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])
    return []


def get_bfs_path():
    graph = _current_adjacency_graph()
    start = global_game_data.start_node
    target = global_game_data.target_node
    exit_node = global_game_data.exit_node

    segment1 = _bfs_segment(graph, start, target)
    segment2 = _bfs_segment(graph, target, exit_node)

    full_path = segment1 + segment2[1:]

    assert segment1, "No path from start to target"
    assert segment2, "No path from target to exit"
    assert full_path[0] == start

    assert_path_postconditions(graph, full_path, target, exit_node)
    return full_path
    
def _dijkstra_segment(graph, start, goal):
    """Helper to perform Dijkstra's search from start to goal"""
    pq = [(0, [start])]
    distances = {start: 0}

    while pq:
        current_cost, path = heapq.heappop(pq)
        node = path[-1]

        if node == goal:
            return path
        if current_cost > distances.get(node, float('inf')):
            continue
        for neighbor in graph.get(node, []):
            new_cost = current_cost + 1
            if new_cost < distances.get(neighbor, float('inf')):
                distances[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, path + [neighbor]))

    return []


def get_dijkstra_path():
    graph = _current_adjacency_graph()
    start = global_game_data.start_node
    target = global_game_data.target_node
    exit_node = global_game_data.exit_node

    segment1 = _dijkstra_segment(graph, start, target)
    segment2 = _dijkstra_segment(graph, target, exit_node)

    full_path = segment1 + segment2[1:]

    assert_path_postconditions(graph, full_path, target, exit_node)
    return full_path
