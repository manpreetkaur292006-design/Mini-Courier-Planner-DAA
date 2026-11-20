# data.py
# This file stores our parcels and our road map (graph).


class Parcel:
    """
    A Parcel object stores all details about one parcel.
    """

    def __init__(self, parcel_id, weight, value, deadline, location):
        self.parcel_id = parcel_id    # name of the parcel, e.g. "P1"
        self.weight = weight          # weight in kg
        self.value = value            # importance / profit of the parcel
        self.deadline = deadline      # days left to deliver
        self.location = location      # node number in the graph

    def show(self):
        # Prints the parcel details in one readable line
        print("Parcel", self.parcel_id,
              "| weight:", self.weight,
              "| value:", self.value,
              "| deadline:", self.deadline,
              "| location:", self.location)


def get_sample_parcels():
    """
    Creates and returns a list of sample parcels.
    """
    parcels = []

    parcels.append(Parcel("P1", 5, 60, 2, 1))
    parcels.append(Parcel("P2", 3, 40, 1, 2))
    parcels.append(Parcel("P3", 4, 50, 3, 3))
    parcels.append(Parcel("P4", 6, 70, 2, 4))
    parcels.append(Parcel("P5", 2, 30, 4, 5))
    parcels.append(Parcel("P6", 7, 80, 5, 3))

    return parcels


def add_road(graph, node_a, node_b, distance):
    """
    Adds a two-way road between node_a and node_b.
    A two-way road means we store it in both directions.
    """
    if node_a not in graph:
        graph[node_a] = []
    if node_b not in graph:
        graph[node_b] = []

    graph[node_a].append((node_b, distance))
    graph[node_b].append((node_a, distance))


def get_sample_graph():
    """
    Builds the road map. Node 0 is the depot.
    Graph format: {node: [(neighbor, distance), ...]}
    """
    graph = {}

    add_road(graph, 0, 1, 4)
    add_road(graph, 0, 2, 2)
    add_road(graph, 1, 2, 1)
    add_road(graph, 1, 3, 5)
    add_road(graph, 2, 3, 8)
    add_road(graph, 2, 4, 10)
    add_road(graph, 3, 4, 2)
    add_road(graph, 3, 5, 6)
    add_road(graph, 4, 5, 3)

    return graph


# This part runs only when you run data.py directly (for testing)
if __name__ == "__main__":
    my_parcels = get_sample_parcels()
    print("--- Parcels ---")
    for parcel in my_parcels:
        parcel.show()

    my_graph = get_sample_graph()
    print()
    print("--- Graph ---")
    for node in my_graph:
        print("Node", node, "->", my_graph[node])