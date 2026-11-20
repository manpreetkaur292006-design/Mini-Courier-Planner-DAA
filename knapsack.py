# knapsack.py
# Chooses the best set of parcels for one trip using 0/1 Knapsack (Dynamic Programming).

from data import get_sample_parcels
from sorting import merge_sort


def knapsack(parcels, capacity):
    """
    parcels  : list of Parcel objects
    capacity : maximum weight the van can carry
    Returns  : (best_value, list_of_selected_parcels, table)
    """
    n = len(parcels)

    # Step 1: create the table with (n+1) rows and (capacity+1) columns, all zeros
    table = []
    for i in range(n + 1):
        row = []
        for w in range(capacity + 1):
            row.append(0)
        table.append(row)

    # Step 2: fill the table
    for i in range(1, n + 1):
        current_parcel = parcels[i - 1]    # row i matches parcel number i-1 in the list

        for w in range(capacity + 1):
            # Choice 1: skip this parcel
            value_if_skipped = table[i - 1][w]

            # Choice 2: take this parcel (only possible if it fits)
            if current_parcel.weight <= w:
                remaining_weight = w - current_parcel.weight
                value_if_taken = current_parcel.value + table[i - 1][remaining_weight]
            else:
                value_if_taken = 0

            # Keep the better choice
            if value_if_taken > value_if_skipped:
                table[i][w] = value_if_taken
            else:
                table[i][w] = value_if_skipped

    # Step 3: the answer is in the bottom-right corner
    best_value = table[n][capacity]

    # Step 4: backtrack to find which parcels were selected
    selected_parcels = []
    w = capacity

    for i in range(n, 0, -1):
        # If the value changed compared to the row above, parcel i was taken
        if table[i][w] != table[i - 1][w]:
            taken_parcel = parcels[i - 1]
            selected_parcels.append(taken_parcel)
            w = w - taken_parcel.weight

    # We collected parcels from last to first, so reverse the list
    selected_parcels.reverse()

    return best_value, selected_parcels, table


def print_table(parcels, table, capacity):
    """
    Prints the DP table so you can see it (good evidence for the report).
    """
    print("DP table (rows = parcels considered, columns = weight limit 0 to", capacity, ")")

    header = "          "
    for w in range(capacity + 1):
        header = header + str(w).rjust(4)
    print(header)

    for i in range(len(table)):
        if i == 0:
            label = "none"
        else:
            label = parcels[i - 1].parcel_id

        line = label.ljust(10)
        for w in range(capacity + 1):
            line = line + str(table[i][w]).rjust(4)
        print(line)


# This part runs only when you run knapsack.py directly
if __name__ == "__main__":
    van_capacity = 15

    all_parcels = get_sample_parcels()
    sorted_parcels = merge_sort(all_parcels)

    best_value, chosen, dp_table = knapsack(sorted_parcels, van_capacity)

    print_table(sorted_parcels, dp_table, van_capacity)

    print()
    print("Van capacity:", van_capacity, "kg")
    print("Best total value:", best_value)
    print("Selected parcels:")

    total_weight = 0
    for parcel in chosen:
        parcel.show()
        total_weight = total_weight + parcel.weight

    print("Total weight carried:", total_weight, "kg")