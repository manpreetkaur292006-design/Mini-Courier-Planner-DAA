# graph.py
# Dijkstra's algorithm: shortest distance from one node to all other nodes.

import heapq

from data import get_sample_graph


def dijkstra(graph, start):
    """
    graph : dictionary {node: [(neighbor, distance), ...]}
    start : the node we start from
    Returns: (distances, previous)
      distances[node] = shortest distance from start to node
      previous[node]  = the node just before 'node' on the shortest path
    """
    # Step 1: every node starts with a very large distance
    distances = {}
    previous = {}
    for node in graph:
        distances[node] = float("inf")
        previous[node] = None

    distances[start] = 0

    # The priority queue holds pairs of (distance, node)
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))

    # Step 2: keep processing until the queue is empty
    while len(priority_queue) > 0:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we already found a shorter way to this node, skip this old entry
        if current_distance > distances[current_node]:
            continue

        # Step 3: look at every neighbor of the current node
        for neighbor, road_length in graph[current_node]:
            new_distance = current_distance + road_length

            # Relaxation: is this new way shorter?
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

    return distances, previous


def get_path(previous, start, target):
    """
    Builds the actual path (list of nodes) from start to target
    by walking backwards using the 'previous' dictionary.
    """
    path = []
    node = target

    while node is not None:
        path.append(node)
        node = previous[node]

    path.reverse()

    # If the first node is not the start, the target was unreachable
    if path[0] != start:
        return []

    return path


def all_pairs_distances(graph, nodes):
    """
    Runs Dijkstra from each node in 'nodes' and builds a distance table.
    result[a][b] = shortest distance from a to b.
    We will use this in the TSP step.
    """
    result = {}
    for node in nodes:
        distances, previous = dijkstra(graph, node)
        result[node] = distances
    return result


# This part runs only when you run graph.py directly
if __name__ == "__main__":
    my_graph = get_sample_graph()

    distances, previous = dijkstra(my_graph, 0)

    print("--- Shortest distances from depot (node 0) ---")
    for node in sorted(distances):
        path = get_path(previous, 0, node)
        print("Node", node, "| distance:", distances[node], "| path:", path)

    print()
    print("--- Distance table for nodes 0, 2, 3, 4, 5 ---")
    table = all_pairs_distances(my_graph, [0, 2, 3, 4, 5])
    for a in table:
        line = "From " + str(a) + ": "
        for b in table:
            line = line + str(table[a][b]).rjust(4)
        print(line)