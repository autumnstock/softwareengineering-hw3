# Homework 3 - Graph Traversal Game
# Autumn Stock

## Customer Requirements and Interpretations

### 1. Random Pathing Algorithm
- Interpretation: A valid path consists of two connected sub-paths concatonated together- 'Start -> Target' and 'Target -> Exit'.
-Loop Prevention and Revisiting: To prevent infinite loops, the random path generator avoids immediate back-tracking and tracks visited nodes per segment. Nodes can be revisited if necessary to reach an otherwise blocked exit or target, but sequential transitions must exist as valid edges in the graph.
###2. Derived Requirement: Additional Statistic
-User Story: "I want to see another statistic for each player on the scoreboard"
-Derived Requirement: The scoreboard will track and display "Nodes Visited" (total num vertex hops in a player's path, including duplicate visits) alonside distance travelled.
