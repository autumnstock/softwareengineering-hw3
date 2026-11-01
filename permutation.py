"""Steinhaus–Johnson–Trotter permutations and Hamiltonian-cycle detection.

Start is node 0 and Exit is the last node. Cycles and cliques are checked only
on the intermediate nodes 1 .. n-1.
"""

from math import hypot

import graph_data


MAX_SJT_INTERMEDIATE = 10
MAX_CLIQUE_INTERMEDIATE = 16


class SJTElement:
    def __init__(self, value, direction=-1):
        self.value = value
        self.direction = direction


def generate_permutations(elements):
    """Yield every permutation of `elements` using SJT (adjacent transpositions)."""
    arr = [SJTElement(v, -1) for v in sorted(elements)]
    n = len(arr)

    if n == 0:
        yield []
        return

    yield [e.value for e in arr]

    while True:
        mobile_idx = -1
        mobile_val = -1

        for i in range(n):
            val = arr[i].value
            direction = arr[i].direction
            target_idx = i + direction

            if 0 <= target_idx < n and val > arr[target_idx].value:
                if val > mobile_val:
                    mobile_val = val
                    mobile_idx = i

        if mobile_idx == -1:
            break

        target_idx = mobile_idx + arr[mobile_idx].direction
        arr[mobile_idx], arr[target_idx] = arr[target_idx], arr[mobile_idx]

        for i in range(n):
            if arr[i].value > mobile_val:
                arr[i].direction *= -1

        yield [e.value for e in arr]


def _neighbor_keys(neighbors):
    if neighbors is None:
        return []
    if isinstance(neighbors, dict):
        return list(neighbors.keys())
    return list(neighbors)


def _normalize_graph(raw_graph):
    """Accept graph_data list format, dict adjacency lists, or weighted dicts."""
    adjacency = {}
    coordinates = {}
    weights = {}

    if isinstance(raw_graph, dict):
        node_ids = list(raw_graph.keys())
        for node, neighbors in raw_graph.items():
            adjacency[node] = _neighbor_keys(neighbors)
            if isinstance(neighbors, dict):
                weights[node] = dict(neighbors)
        start_node = 0 if 0 in adjacency else min(node_ids)
        exit_node = max(node_ids)
        return adjacency, coordinates, weights, start_node, exit_node

    for index, node in enumerate(raw_graph):
        coordinates[index] = (float(node[0][0]), float(node[0][1]))
        adjacency[index] = list(node[1])

    start_node = 0
    exit_node = len(raw_graph) - 1
    return adjacency, coordinates, weights, start_node, exit_node


def powerset(nodes):
    """Recursive powerset. Does not use itertools or other subset helpers."""
    if not nodes:
        return [[]]
    head = nodes[0]
    rest = powerset(nodes[1:])
    return rest + [[head] + subset for subset in rest]


class SJTGraphSolver:
    def __init__(self, raw_graph):
        (
            self.adjacency,
            self.coordinates,
            self.weights,
            self.start_node,
            self.exit_node,
        ) = _normalize_graph(raw_graph)

    def intermediate_nodes(self):
        return [
            node
            for node in sorted(self.adjacency.keys())
            if node != self.start_node and node != self.exit_node
        ]

    def generate_permutations(self, elements):
        return generate_permutations(elements)

    def has_edge(self, u, v):
        return v in self.adjacency.get(u, [])

    def edge_distance(self, u, v):
        if u in self.weights and v in self.weights[u]:
            return float(self.weights[u][v])
        if u in self.coordinates and v in self.coordinates:
            x1, y1 = self.coordinates[u]
            x2, y2 = self.coordinates[v]
            return hypot(x2 - x1, y2 - y1)
        return 1.0

    def cycle_distance(self, cycle):
        total = 0.0
        for u, v in zip(cycle[:-1], cycle[1:]):
            total += self.edge_distance(u, v)
        return total

    def is_valid_hamiltonian_cycle(self, permutation):
        """True iff `permutation` is a cycle through every intermediate node."""
        if len(permutation) < 3:
            return False
        if sorted(permutation) != self.intermediate_nodes():
            return False

        for i in range(len(permutation)):
            u = permutation[i]
            v = permutation[(i + 1) % len(permutation)]
            if not self.has_edge(u, v):
                return False
        return True

    def _valid_cycles_with_distance(self):
        nodes = self.intermediate_nodes()
        if len(nodes) < 3:
            return []

        found = []
        for perm in generate_permutations(nodes):
            if self.is_valid_hamiltonian_cycle(perm):
                cycle = list(perm) + [perm[0]]
                found.append((cycle, self.cycle_distance(cycle)))
        return found

    def find_all_cycles(self):
        """All Hamiltonian cycles on nodes 1..n-1, or -1 if none exist."""
        cycles = [cycle for cycle, _distance in self._valid_cycles_with_distance()]
        return cycles if cycles else -1

    def find_optimal_cycles(self):
        """Hamiltonian cycles of minimum total distance (ties kept)."""
        found = self._valid_cycles_with_distance()
        if not found:
            return -1, -1

        min_distance = min(distance for _cycle, distance in found)
        optimal = [cycle for cycle, distance in found if distance == min_distance]
        return optimal, min_distance

    def _is_clique(self, subset):
        if len(subset) <= 1:
            return True
        for i in range(len(subset)):
            for j in range(i + 1, len(subset)):
                u = subset[i]
                v = subset[j]
                if not (self.has_edge(u, v) and self.has_edge(v, u)):
                    return False
        return True

    def find_largest_clique(self):
        """Largest clique on intermediate nodes (start and exit excluded)."""
        nodes = self.intermediate_nodes()
        largest = []
        max_size = 0

        for subset in powerset(nodes):
            if self._is_clique(subset) and len(subset) > max_size:
                max_size = len(subset)
                largest = subset

        return largest, max_size


def report_graph(index, raw_graph):
    solver = SJTGraphSolver(raw_graph)
    intermediate = solver.intermediate_nodes()
    n_nodes = len(solver.adjacency)
    print(
        f"Graph {index}: {n_nodes} nodes "
        f"(start={solver.start_node}, exit={solver.exit_node}, "
        f"intermediate={len(intermediate)})"
    )

    if len(intermediate) > MAX_SJT_INTERMEDIATE:
        print(
            f"  Hamiltonian cycles: skipped "
            f"({len(intermediate)}! is too large; cap is {MAX_SJT_INTERMEDIATE})"
        )
    else:
        cycles = solver.find_all_cycles()
        if cycles == -1:
            print("  Hamiltonian cycles: -1")
        else:
            optimal, min_distance = solver.find_optimal_cycles()
            optimal_keys = {tuple(cycle) for cycle in optimal}
            print(f"  Hamiltonian cycles ({len(cycles)}):")
            for cycle in cycles:
                marker = "  [optimal]" if tuple(cycle) in optimal_keys else ""
                print(f"    {cycle}{marker}")
            print(f"  Optimal distance: {min_distance}")

    if len(intermediate) > MAX_CLIQUE_INTERMEDIATE:
        print(
            f"  Largest clique: skipped "
            f"(2^{len(intermediate)} subsets; cap is {MAX_CLIQUE_INTERMEDIATE})"
        )
    else:
        clique, size = solver.find_largest_clique()
        print(f"  Largest clique: {clique} (size {size})")
    print()


if __name__ == "__main__":
    for index, raw_graph in enumerate(graph_data.graph_data):
        report_graph(index, raw_graph)
