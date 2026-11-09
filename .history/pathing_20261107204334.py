import graph_data
import global_game_data
import random
import heapq
import math
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
    global_game_data.graph_paths.append(get_dijkstra_path())

def _edge_distance(u, v):
    """Calculate Euclidean distance between two connected nodes."""
    raw = graph_data.graph_data[global_game_data.current_graph_index]

    x1, y1 = raw[u][0]
    x2, y2 = raw[v][0]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


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
    visited = set()

    while stack:
        path = stack.pop()
        node = path[-1]

        if node == goal:
            return path
        
        if node not in visited:
            visited.add(node)

            for neighbor in sorted(graph.get(node, []), reverse=True):
                if neighbor not in visited:
                    stack.append(path + [neighbor])
    return []

def _a_start_segment(graph, start, goal):
    """Find shortest path using A* search"""

    pq = [(0, start)]

    distances = {start: 0}
    parents = {start: None}

    while pq:
        current_priority, node = heapq.heappop(pq)

        expected_priority = (
            distances[node] + _edge_distance(node, goal)
        )

        if current_priority > expected_priority:
            continue

        if node == goal:
            break

        for neighbor in graph.get(node, []):
            edge_cost = _edge_distance(node, neighbor)
            new_cost = distances[node] + edge_cost

            if new_cost < distances.get(neighbor, float("inf")):
                distances[neighbor] == new_cost
                parents[neighbor] = node

                heuristic = _edge_distance(neighbor, goal)
                priority = new_cost + heuristic

                heapq.heappush(pq, (priority, neighbor))

    if goal not in distances:
        return []

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()
    return path


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
    
    # Priority queue stores (distance, node)
    pq = [(0, start)]

    # Track shortest known distance to each node
    distances = {start: 0}
    
    # Track parent nodes to recontruct shortest path
    parents = {start: None}

    while pq:
        current_cost, node = heapq.heappop(pq)
        if current_cost > distances[node]:
            continue
        if node == goal:
            break
        for neighbor in graph.get(node, []):
            edge_cost = _edge_distance(node, neighbor)
            new_cost = current_cost + edge_cost

            if new_cost < distances.get(neighbor, float("inf")):
                distances[neighbor] = new_cost
                parents[neighbor] = node

                heapq.heappush(pq, (new_cost, neighbor))

    if goal not in distances:
        return []

    path = []
    current = goal

    while current is not None:
        path.append(current)
        current = parents[current]

    path.reverse()

    return path


def get_dijkstra_path():
    """Find shortest path from Start to Target to Exit"""

    graph = _current_adjacency_graph()

    start = global_game_data.start_node
    target = global_game_data.target_node
    exit_node = global_game_data.exit_node

    # Shortest path from Start to Target
    segment1 = _dijkstra_segment(graph, start, target)

    # Shortest path from Target to Exit
    segment2 = _dijkstra_segment(graph, target, exit_node)

    assert segment1, "No path from start to target"
    assert segment2, "No path from target to exit"

    full_path = segment1 + segment2[1:]

    # Postconditions
    assert full_path[0] == start, "Path must begin at Start"
    assert target in full_path, "Path must contain Target"
    assert full_path[-1] == exit_node, "Path must end at Exit"

    for u, v in zip(full_path[:-1], full_path[1:]):
        assert v in graph.get(u, []), (
            f"No edge between nodes {u} and {v}"
        )

    return full_path

def get_a_star_path():
    """Find shortest path from start to target to exit using A*"""

    graph = _current_adjacency_graph()

    start = global_game_data.start_node
    target = global_game_data.target_node
    exit_node = global_game_data.exit_node

    segment1 = _a_start_segment(graph, start, target)
    segment2 = _a_start_segment(graph, target, exit_node)

    assert segment1, "No path from start to target"
    assert segment2, "No path from target to exit"

    full_path = segment1 + segment2[1:]

    assert full_path[0] == start, "Path must begin at Start"
    assert target in full_path, "Path must contain Target"
    assert full_path[-1] == exit_node, "Path must end at Exit"

    for u, v in zip(full_path[:-1], full_path[1:]):
        assert v in graph.get(u, []), (
            f"No edge between {u} and {v}"
        )

    return full_path

