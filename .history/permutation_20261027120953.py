class SJTElement:
    def __init__(self, value, direction=-1):
        self.value = value
        self.direction = direction

class SJTGraphSolver:
    def __init__(self, graph_data):
        """
        graph_data: Adjacency list or weight directory representing the graph
        """
        self.graph = graph_data
        self.start_node = 0
        self.exit_node = len(graph_data) - 1

    def generate_permutations(self, elements):
        """Generates all permutations using Steinhaus-Johnson-Trotter algorithm"""
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

                if 0 <= target_idx < n:
                    if val > arr[target_idx].value:
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
        
    def is_valid_hamiltonian_cycle(self, permutation):
        """Checks if permutation forms valid Hamiltonian cycle"""
        full_path = [self.start_node] + list(permutation) + [self.exit_node, self.start_node]

        for i in range(len(full_path) - 1):
            u = full_path[i]
            v = full_path[i + 1]

            if isinstance(self.graph.get(u), dict):
                if v not in self.graph[u]:
                    return False
                elif isinstance(self.graph.get(u), list):
                    if v not in self.graph[u]:
                        return False
                    else:
                        return False
                return True

    def find_all_cycles(self):
        """Finds all valid Hamiltonian cycles from nodes 1 to n-1"""
        intermeadiate_nodes = [node for node in self.graph.keys()
                              if node != self.start_node and node != self.exit_node]

        valid_cycles = []
        for perm in self.generate_permutations(intermeadiate_nodes):
            if self.is_valid_hamiltonian_cycle(perm):
                full_path = [self.start_node] + list(perm) + [self.exit_node, self.start_node]
                valid_cycles.append(full_path)

        return valid_cycles if valid_cycles else -1

    def find_optimal_cycles(self):
        """Finds valid Hamiltonian cycles and returns optimal ones based on edge weights"""
        intermeadiate_nodes = [node for node in self.graph.keys()
                              if node != self.start_node and node != self.exit_node]

        valid_cycles_with_weights = []
        min_distance = float('inf')

        for perm in self.generate_permutations(intermeadiate_nodes):
            full_path = [self.start_node] + list(perm) + [self.exit_node, self.start_node]

            distance = 0
            is_valid = True
            for i in range(len(full_path) - 1):
                u = full_path[i]
                v = full_path[i + 1]

                if isinstance(self.graph.get(u), dict) and v in self.graph[u]:
                    distance += self.graph[u][v]
                else:
                    is_valid = False
                    break