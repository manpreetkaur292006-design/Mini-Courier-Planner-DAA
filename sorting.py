# sorting.py
# Sorts parcels by deadline using Merge Sort.

from data import get_sample_parcels


def is_before(parcel_a, parcel_b):
    """
    Decides if parcel_a should come BEFORE parcel_b.
    Rule 1: smaller deadline comes first (more urgent).
    Rule 2: if deadlines are equal, higher value comes first.
    """
    if parcel_a.deadline < parcel_b.deadline:
        return True

    if parcel_a.deadline > parcel_b.deadline:
        return False

    # Deadlines are equal, so compare the values
    if parcel_a.value >= parcel_b.value:
        return True

    return False


def merge(left_list, right_list):
    """
    Merges two already-sorted lists into one sorted list.
    """
    merged = []
    i = 0   # pointer for left_list
    j = 0   # pointer for right_list

    # Keep going while both lists still have items
    while i < len(left_list) and j < len(right_list):
        if is_before(left_list[i], right_list[j]):
            merged.append(left_list[i])
            i = i + 1
        else:
            merged.append(right_list[j])
            j = j + 1

    # One list may still have leftover items, so copy them
    while i < len(left_list):
        merged.append(left_list[i])
        i = i + 1

    while j < len(right_list):
        merged.append(right_list[j])
        j = j + 1

    return merged


def merge_sort(parcels):
    """
    Sorts a list of parcels using Merge Sort.
    """
    # Base case: a list with 0 or 1 item is already sorted
    if len(parcels) <= 1:
        return parcels

    # Step 1: split the list into two halves
    middle = len(parcels) // 2
    left_half = parcels[:middle]
    right_half = parcels[middle:]

    # Step 2: sort each half (recursion)
    sorted_left = merge_sort(left_half)
    sorted_right = merge_sort(right_half)

    # Step 3: merge the two sorted halves
    return merge(sorted_left, sorted_right)


# This part runs only when you run sorting.py directly
if __name__ == "__main__":
    my_parcels = get_sample_parcels()

    print("--- Before sorting ---")
    for parcel in my_parcels:
        parcel.show()

    sorted_parcels = merge_sort(my_parcels)

    print()
    print("--- After sorting (most urgent first) ---")
    for parcel in sorted_parcels:
        parcel.show()