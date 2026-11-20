# main.py
# Mini-Courier Planner: runs the complete pipeline
# Sort -> Knapsack -> Dijkstra -> Nearest-Neighbor TSP

from data import get_sample_parcels, get_sample_graph
from sorting import merge_sort
from knapsack import knapsack, print_table
from graph import dijkstra, get_path, all_pairs_distances
from route import get_delivery_points, nearest_neighbor_route


def build_full_path(graph, route):
    """
    The TSP route only lists delivery points, for example [0, 2, 3, 4, 5, 0].
    Roads between them may pass through other nodes (like node 1).
    This function expands each leg into the real road path using Dijkstra.
    """
    full_path = [route[0]]

    for i in range(len(route) - 1):
        start_node = route[i]
        end_node = route[i + 1]

        distances, previous = dijkstra(graph, start_node)
        leg_path = get_path(previous, start_node, end_node)

        # leg_path begins with start_node, which is already in full_path, so skip it
        for j in range(1, len(leg_path)):
            full_path.append(leg_path[j])

    return full_path


def main():
    van_capacity = 15
    depot = 0

    parcels = get_sample_parcels()
    graph = get_sample_graph()

    print("=" * 60)
    print("MINI-COURIER PLANNER")
    print("=" * 60)

    # ---------- Stage 1: sorting ----------
    print()
    print("STAGE 1: Parcels sorted by deadline (most urgent first)")
    sorted_parcels = merge_sort(parcels)
    for parcel in sorted_parcels:
        parcel.show()

    # ---------- Stage 2: knapsack ----------
    print()
    print("STAGE 2: Knapsack - best parcels for one trip (capacity", van_capacity, "kg)")
    best_value, chosen, table = knapsack(sorted_parcels, van_capacity)
    print_table(sorted_parcels, table, van_capacity)
    print()
    print("Best total value:", best_value)
    print("Selected parcels:")
    total_weight = 0
    for parcel in chosen:
        parcel.show()
        total_weight = total_weight + parcel.weight
    print("Total weight carried:", total_weight, "kg")

    # ---------- Stage 3: Dijkstra ----------
    print()
    print("STAGE 3: Dijkstra - shortest distances")
    points = get_delivery_points(chosen)
    needed_nodes = [depot] + points
    distance_table = all_pairs_distances(graph, needed_nodes)

    print("Delivery points:", points)
    for a in needed_nodes:
        line = "From " + str(a).rjust(2) + ": "
        for b in needed_nodes:
            line = line + str(distance_table[a][b]).rjust(4)
        print(line)
    print("(column order:", needed_nodes, ")")

    # ---------- Stage 4: TSP ----------
    print()
    print("STAGE 4: Nearest-Neighbor TSP route")
    route, total = nearest_neighbor_route(distance_table, depot, points)
    print("Delivery order:", route)

    # Show each leg with its distance, so the total is easy to verify
    print("Leg by leg:")
    for i in range(len(route) - 1):
        a = route[i]
        b = route[i + 1]
        print("  ", a, "->", b, ":", distance_table[a][b])
    print("Total route length:", total)

    full_path = build_full_path(graph, route)
    print("Actual road path (including pass-through nodes):", full_path)

    print()
    print("=" * 60)
    print("Done.")


main()