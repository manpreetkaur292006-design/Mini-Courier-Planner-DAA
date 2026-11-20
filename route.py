# route.py
# Plans the delivery route using the Nearest-Neighbor TSP approximation.

from data import get_sample_parcels, get_sample_graph
from sorting import merge_sort
from knapsack import knapsack
from graph import all_pairs_distances


def get_delivery_points(selected_parcels):
    """
    Collects the unique delivery locations from the selected parcels.
    Two parcels can go to the same location, so we avoid duplicates.
    """
    points = []
    for parcel in selected_parcels:
        if parcel.location not in points:
            points.append(parcel.location)
    return points


def nearest_neighbor_route(distance_table, depot, delivery_points):
    """
    distance_table  : result[a][b] = shortest distance from a to b
    depot           : starting node (0)
    delivery_points : list of nodes we must visit
    Returns: (route, total_distance)
    """
    route = [depot]
    total_distance = 0
    current = depot

    # Copy the list so we do not change the original
    unvisited = []
    for point in delivery_points:
        unvisited.append(point)

    # Keep going until every delivery point is visited
    while len(unvisited) > 0:
        nearest_point = None
        nearest_distance = float("inf")

        # Find the closest unvisited point from where we are now
        for point in unvisited:
            d = distance_table[current][point]
            if d < nearest_distance:
                nearest_distance = d
                nearest_point = point

        route.append(nearest_point)
        total_distance = total_distance + nearest_distance
        unvisited.remove(nearest_point)
        current = nearest_point

    # Return to the depot
    total_distance = total_distance + distance_table[current][depot]
    route.append(depot)

    return route, total_distance


# This part runs only when you run route.py directly
if __name__ == "__main__":
    van_capacity = 15
    depot = 0

    parcels = get_sample_parcels()
    graph = get_sample_graph()

    # Stage 1: sort
    sorted_parcels = merge_sort(parcels)

    # Stage 2: knapsack
    best_value, chosen, table = knapsack(sorted_parcels, van_capacity)

    print("Selected parcels:")
    for parcel in chosen:
        parcel.show()

    # Stage 3: shortest distances between all needed nodes
    points = get_delivery_points(chosen)
    needed_nodes = [depot] + points
    distance_table = all_pairs_distances(graph, needed_nodes)

    # Stage 4: route
    route, total = nearest_neighbor_route(distance_table, depot, points)

    print()
    print("Delivery points:", points)
    print("Route:", route)
    print("Total route length:", total)