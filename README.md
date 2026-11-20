🚚 Mini-Courier Planner

Name: Manpreet Kaur | 2501010070 | Language: Python 3

📌 Problem Statement

Given a list of parcels and delivery points, generate a prioritized parcel list, an optimized packing plan and an ordered delivery route, using sorting, dynamic programming, graph algorithms and approximation.

🎯 Phase 1: Design and Planning
Parcels → [1] Merge Sort → [2] 0/1 Knapsack (DP) → [3] Dijkstra → [4] Nearest-Neighbor TSP → Route
Stage	Algorithm	Complexity	Why
🔢 Prioritize	Merge Sort	O(n log n)	Stable, same speed in every case
📦 Pack	0/1 Knapsack	O(n × W)	Van has a weight limit
🗺️ Distances	Dijkstra (heap)	O((V+E) log V)	Real shortest road distance
🛣️ Route	Nearest-Neighbor	O(k²)	Fast approximation of TSP
Parcel: id, weight (kg), value, deadline (days), location (graph node)
Graph: adjacency list {node: [(neighbor, distance), ...]}, node 0 is the depot, roads are two-way.
Sample data: 6 parcels (P1 to P6), 6 nodes, 9 roads, van capacity 15 kg (see data.py). 📸 screenshots/data.py.png
📦 Phase 2: Prioritization and Box Filling
Sorting rule: smaller deadline first; on a tie, higher value first. Result: P2 → P4 → P1 → P3 → P5 → P6. 📸 screenshots/sorting.py.png
Knapsack: table[i][w] = best value using the first i parcels with limit w. Chosen parcels are found by backtracking. Result: P2, P4, P3, P5, weight 15 kg, value 190. 📸 screenshots/knapsack.py.png
🗺️ Phase 3: Route Maker and Graph Processing
Dijkstra from depot: node 1 = 3, node 2 = 2, node 3 = 8, node 4 = 10, node 5 = 13. 📸 screenshots/graph.py.png
Nearest-Neighbor TSP over delivery points [2, 4, 3, 5]: 0 → 2 → 3 → 4 → 5 → 0 = 2 + 6 + 2 + 3 + 13 = 26
Actual road path: [0, 2, 1, 3, 4, 5, 4, 3, 1, 2, 0] (passes through node 1). 📸 screenshots/route.py.png, screenshots/main.py.png
⏱️ Phase 4: Performance Testing and Optimization

Each stage was timed with time.perf_counter() (best of 3 runs). Times in milliseconds:

Parcels	Merge Sort	Built-in sort	Knapsack 2D	Knapsack 1D	Dijkstra	TSP	Correct
10	0.009	0.001	0.04	0.01	0.13	0.003	✅
50	0.049	0.007	0.53	0.24	0.88	0.010	✅
100	0.101	0.014	2.08	0.75	4.35	0.041	✅
200	0.216	0.027	8.55	3.25	18.04	0.133	✅
400	0.466	0.060	34.83	13.22	83.53	0.993	✅

Runtime chart Comparison chart

Correctness: DP matched brute force in 5/5 random trials; sorting matched Python's sorted(); capacity was never exceeded; every route starts and ends at the depot and visits each stop once. 📸 screenshots/performance.py.png

Findings: built-in sort is about 8x faster than merge sort (C implementation); 1D knapsack is about 2.6x faster than 2D; Dijkstra is the slowest stage because it runs once per delivery point.

Suggested improvements: use 1D knapsack when only the value is needed, use built-in sort in production, run Dijkstra only when needed, improve the route with 2-opt, and raise the value of urgent parcels.

🏁 Phase 5: Result Explanation
Why not P6? It has the highest value (80) but the lowest value per kg (about 11.4). Knapsack picks the best combination, and P2, P4, P3, P5 fill exactly 15 kg for 190.
Why return to depot? The route is a closed tour: the van starts and ends at the depot.
Why only approximate? Greedy choices can leave a long trip back; here the last leg 5 → 0 costs 13.
Limitation: knapsack maximizes value, not deadlines, so an urgent parcel (like P1) can be left out.
📁 Files

data.py sorting.py knapsack.py graph.py route.py main.py performance.py results.txt runtime_chart.png comparison_chart.png screenshots/

▶️ How to Run
Install Python 3 (tick "Add to PATH") and matplotlib: py -m pip install matplotlib
Full planner: py main.py
Tests, timings and charts: py performance.py

💡 On Windows, use py if python is not recognized.