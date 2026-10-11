# Homework 3 - Graph Traversal Game
# Autumn Stock

## Customer Requirements and Interpretations

### 1. Random Pathing Algorithm
- Interpretation: A valid path consists of two connected sub-paths concatonated together- 'Start -> Target' and 'Target -> Exit'.
-Loop Prevention and Revisiting: The algorithm uses randomized depth-first exploration. At each node it randomly selects an unvisited neighbor. If it reaches a dead-end, it backtracks and explore another option. Tracking visied nodes prevents infinite loops, while backtracking allows the algoritm to find another route when necessary. Each generated path must begin at a start node, include a target node, end at the exit node and contain only valid edges between consecutive nodes.
### 2. Derived Requirement: Additional Statistic
-User Story: "I want to see another statistic for each player on the scoreboard"
-Derived Requirement: The scoreboard will display the number of nodes visited by each player during traversal. The Nodes Visited statistic starts at one for the starting node and increases each time the player reaches another node. Repeated vists are counted seperately.

### 3. BFS and DFS
-BFS uses a queue to explore neighboring nodes level by level, finding paths with the fewest edges in the unweighted graph.
-DFS uses a stack to explore paths deeply before considering alternatives. Does not guarantee the shortest path.

### 4. Winner Determination
-Winning player in the player whose valid path from start to target to exit has the shortest total geometric distance, calculated using the coordinates of consecutive nodes. The test player is only eligible if its path includes the target node. 
