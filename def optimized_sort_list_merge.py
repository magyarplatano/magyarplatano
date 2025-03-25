def optimized_sort_list_merge(list_to_sort):
    """
    Sorts a list using the Merge Sort algorithm.
    """
    if len(list_to_sort) <= 1:
        return list_to_sort.copy()  # Avoid modifying original

    mid = len(list_to_sort) // 2
    left_half = list_to_sort[:mid]
    right_half = list_to_sort[mid:]

    left_half = optimized_sort_list_merge(left_half)
    right_half = optimized_sort_list_merge(right_half)

    return merge(left_half, right_half)


def merge(left, right):
    """
    Merges two sorted lists into a single sorted list.
    """
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged