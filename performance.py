# performance.py
# Tests the system on small and large datasets, checks correctness,
# records runtimes, compares optimizations, and saves charts.

import random
import time
from itertools import combinations

import matplotlib.pyplot as plt

from data import Parcel, add_road
from sorting import merge_sort
from knapsack import knapsack
from graph import all_pairs_distances
from route import get_delivery_points, nearest_neighbor_route


# ---------------------------------------------------------------
# Data generators
# ---------------------------------------------------------------

def generate_parcels(count, number_of_nodes):
    """Creates 'count' random parcels. Locations are nodes 1 to number_of_nodes - 1."""
    parcels = []
    for i in range(count):
        parcel_id = "P" + str(i + 1)
        weight = random.randint(1, 10)
        value = random.randint(10, 100)
        deadline = random.randint(1, 10)
        location = random.randint(1, number_of_nodes - 1)
        parcels.append(Parcel(parcel_id, weight, value, deadline, location))
    return parcels


def generate_graph(number_of_nodes):
    """Creates a random connected graph (every node is linked to an earlier node first)."""
    graph = {}
    for node in range(number_of_nodes):
        graph[node] = []

    for node in range(1, number_of_nodes):
        earlier_node = random.randint(0, node - 1)
        add_road(graph, node, earlier_node, random.randint(1, 20))

    extra_roads = number_of_nodes * 2
    for i in range(extra_roads):
        a = random.randint(0, number_of_nodes - 1)
        b = random.randint(0, number_of_nodes - 1)
        if a != b:
            add_road(graph, a, b, random.randint(1, 20))

    return graph


# ---------------------------------------------------------------
# Extra functions used for comparison and correctness checking
# ---------------------------------------------------------------

def sort_key(parcel):
    """Same rule as our merge sort: smaller deadline first, then higher value first."""
    return (parcel.deadline, -parcel.value)


def knapsack_1d(parcels, capacity):
    """
    Optimized knapsack: uses ONE row instead of a full table.
    Space is O(W) instead of O(n x W). It returns only the best value
    (it cannot easily tell WHICH parcels were chosen).
    """
    best = []
    for w in range(capacity + 1):
        best.append(0)

    for parcel in parcels:
        # Go from right to left so each parcel is used at most once
        for w in range(capacity, parcel.weight - 1, -1):
            candidate = parcel.value + best[w - parcel.weight]
            if candidate > best[w]:
                best[w] = candidate

    return best[capacity]


def brute_force_knapsack(parcels, capacity):
    """
    Tries EVERY possible group of parcels. Very slow, so use it on small inputs only.
    We use it to prove that our DP answer is correct.
    """
    best_value = 0
    for size in range(len(parcels) + 1):
        for group in combinations(parcels, size):
            total_weight = 0
            total_value = 0
            for parcel in group:
                total_weight = total_weight + parcel.weight
                total_value = total_value + parcel.value
            if total_weight <= capacity and total_value > best_value:
                best_value = total_value
    return best_value


def check_pipeline(parcels, sorted_parcels, chosen, best_value, best_value_1d,
                   capacity, route, points):
    """
    Checks the results of one test. Returns True only if every check passes.
    """
    # Check 1: merge sort gives the same order as Python's sorted()
    expected = sorted(parcels, key=sort_key)
    for i in range(len(expected)):
        if expected[i].parcel_id != sorted_parcels[i].parcel_id:
            return False

    # Check 2: knapsack total weight is within capacity
    total_weight = 0
    total_value = 0
    for parcel in chosen:
        total_weight = total_weight + parcel.weight
        total_value = total_value + parcel.value
    if total_weight > capacity:
        return False

    # Check 3: chosen parcels really add up to best_value, and 1D version agrees
    if total_value != best_value:
        return False
    if best_value != best_value_1d:
        return False

    # Check 4: route starts and ends at depot and visits every point exactly once
    if route[0] != 0 or route[len(route) - 1] != 0:
        return False
    middle = route[1:len(route) - 1]
    if sorted(middle) != sorted(points):
        return False

    return True


# ---------------------------------------------------------------
# Timing one test case
# ---------------------------------------------------------------

def time_one_run(parcel_count, number_of_nodes, capacity):
    """
    Generates data, runs every stage 3 times, and keeps the FASTEST time of the 3
    (this reduces random noise from the computer). Returns a dictionary of results.
    """
    repeats = 3
    parcels = generate_parcels(parcel_count, number_of_nodes)
    graph = generate_graph(number_of_nodes)

    # Stage 1: merge sort (our own)
    sort_time = float("inf")
    for r in range(repeats):
        start = time.perf_counter()
        sorted_parcels = merge_sort(parcels)
        elapsed = time.perf_counter() - start
        if elapsed < sort_time:
            sort_time = elapsed

    # Stage 1b: Python's built-in sorted (for comparison)
    builtin_time = float("inf")
    for r in range(repeats):
        start = time.perf_counter()
        builtin_sorted = sorted(parcels, key=sort_key)
        elapsed = time.perf_counter() - start
        if elapsed < builtin_time:
            builtin_time = elapsed

    # Stage 2: knapsack with full 2D table
    knapsack_time = float("inf")
    for r in range(repeats):
        start = time.perf_counter()
        best_value, chosen, table = knapsack(sorted_parcels, capacity)
        elapsed = time.perf_counter() - start
        if elapsed < knapsack_time:
            knapsack_time = elapsed

    # Stage 2b: knapsack with 1D array (optimized)
    knapsack_1d_time = float("inf")
    for r in range(repeats):
        start = time.perf_counter()
        best_value_1d = knapsack_1d(sorted_parcels, capacity)
        elapsed = time.perf_counter() - start
        if elapsed < knapsack_1d_time:
            knapsack_1d_time = elapsed

    # Stage 3: Dijkstra from the depot and every delivery point
    points = get_delivery_points(chosen)
    needed_nodes = [0] + points
    dijkstra_time = float("inf")
    for r in range(repeats):
        start = time.perf_counter()
        distance_table = all_pairs_distances(graph, needed_nodes)
        elapsed = time.perf_counter() - start
        if elapsed < dijkstra_time:
            dijkstra_time = elapsed

    # Stage 4: nearest-neighbor route
    tsp_time = float("inf")
    for r in range(repeats):
        start = time.perf_counter()
        route, total = nearest_neighbor_route(distance_table, 0, points)
        elapsed = time.perf_counter() - start
        if elapsed < tsp_time:
            tsp_time = elapsed

    passed = check_pipeline(parcels, sorted_parcels, chosen, best_value,
                            best_value_1d, capacity, route, points)

    result = {}
    result["parcels"] = parcel_count
    result["nodes"] = number_of_nodes
    result["capacity"] = capacity
    result["chosen"] = len(chosen)
    result["points"] = len(points)
    result["sort_ms"] = sort_time * 1000
    result["builtin_ms"] = builtin_time * 1000
    result["knapsack_ms"] = knapsack_time * 1000
    result["knapsack_1d_ms"] = knapsack_1d_time * 1000
    result["dijkstra_ms"] = dijkstra_time * 1000
    result["tsp_ms"] = tsp_time * 1000
    result["route_length"] = total
    result["passed"] = passed
    return result


def run_brute_force_test():
    """Proves the DP knapsack is optimal by comparing with brute force on small inputs."""
    print("--- Knapsack correctness test (DP vs brute force, 10 parcels, 5 random trials) ---")
    all_good = True
    for trial in range(5):
        parcels = generate_parcels(10, 20)
        capacity = 25
        dp_value, chosen, table = knapsack(parcels, capacity)
        brute_value = brute_force_knapsack(parcels, capacity)
        if dp_value == brute_value:
            status = "PASS"
        else:
            status = "FAIL"
            all_good = False
        print("Trial", trial + 1, "| DP:", dp_value, "| Brute force:", brute_value, "|", status)
    return all_good


# ---------------------------------------------------------------
# Main program
# ---------------------------------------------------------------

if __name__ == "__main__":
    random.seed(1)    # same random data on every run, so results can be repeated

    run_brute_force_test()
    print()

    # Each test: (number of parcels, number of graph nodes, van capacity)
    test_cases = [
        (10, 20, 30),
        (50, 60, 100),
        (100, 120, 200),
        (200, 250, 400),
        (400, 500, 800),
    ]

    all_results = []
    for parcel_count, number_of_nodes, capacity in test_cases:
        print("Running test:", parcel_count, "parcels,", number_of_nodes, "nodes ...")
        all_results.append(time_one_run(parcel_count, number_of_nodes, capacity))

    # Build the results table as text lines
    lines = []
    lines.append("Parcels | Nodes | Capacity | Chosen | Sort | Built-in | Knap2D | Knap1D | Dijkstra | TSP | Route | Correct")
    lines.append("(all times in milliseconds)")
    for r in all_results:
        line = (str(r["parcels"]).rjust(7) + " | " +
                str(r["nodes"]).rjust(5) + " | " +
                str(r["capacity"]).rjust(8) + " | " +
                str(r["chosen"]).rjust(6) + " | " +
                str(round(r["sort_ms"], 3)).rjust(6) + " | " +
                str(round(r["builtin_ms"], 3)).rjust(8) + " | " +
                str(round(r["knapsack_ms"], 2)).rjust(6) + " | " +
                str(round(r["knapsack_1d_ms"], 2)).rjust(6) + " | " +
                str(round(r["dijkstra_ms"], 2)).rjust(8) + " | " +
                str(round(r["tsp_ms"], 3)).rjust(5) + " | " +
                str(r["route_length"]).rjust(5) + " | " +
                str(r["passed"]))
        lines.append(line)

    print()
    for line in lines:
        print(line)

    # Save the table as evidence for the report
    results_file = open("results.txt", "w")
    for line in lines:
        results_file.write(line + "\n")
    results_file.close()
    print()
    print("Table saved as results.txt")

    # Collect values for the charts
    sizes = []
    sort_times = []
    knapsack_times = []
    dijkstra_times = []
    tsp_times = []
    for r in all_results:
        sizes.append(r["parcels"])
        sort_times.append(r["sort_ms"])
        knapsack_times.append(r["knapsack_ms"])
        dijkstra_times.append(r["dijkstra_ms"])
        tsp_times.append(r["tsp_ms"])

    # Chart 1: runtime of each stage vs input size (log scale so small values stay visible)
    plt.figure(figsize=(8, 5))
    plt.plot(sizes, sort_times, marker="o", label="Merge Sort")
    plt.plot(sizes, knapsack_times, marker="o", label="Knapsack DP")
    plt.plot(sizes, dijkstra_times, marker="o", label="Dijkstra")
    plt.plot(sizes, tsp_times, marker="o", label="Nearest-Neighbor TSP")
    plt.yscale("log")
    plt.xlabel("Number of parcels")
    plt.ylabel("Runtime in milliseconds (log scale)")
    plt.title("Runtime of each stage vs input size")
    plt.legend()
    plt.grid(True)
    plt.savefig("runtime_chart.png")

    # Chart 2: comparison of all steps and optimizations on the LARGEST test
    last = all_results[len(all_results) - 1]
    names = ["Merge Sort", "Built-in sorted", "Knapsack 2D", "Knapsack 1D", "Dijkstra", "TSP"]
    values = [last["sort_ms"], last["builtin_ms"], last["knapsack_ms"],
              last["knapsack_1d_ms"], last["dijkstra_ms"], last["tsp_ms"]]

    plt.figure(figsize=(9, 5))
    plt.bar(names, values)
    plt.yscale("log")
    plt.ylabel("Runtime in milliseconds (log scale)")
    plt.title("Comparison of steps and optimizations (" + str(last["parcels"]) + " parcels)")
    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.savefig("comparison_chart.png")

    print("Charts saved as runtime_chart.png and comparison_chart.png")
    plt.show()