# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# type: ignore
# Import Dependencies
from typing import List


# Swap 2 values in the list by specified indices
def swap(ls, i, j):
    ls[j], ls[i] = ls[i], ls[j]


# Recursive body of the algorithm
def partition(ls, l, h):
    if l < h:
        partition_index = pointer = l - 1
        partition_num = ls[h]
        for el in ls[l:h]:
            pointer += 1
            if el < partition_num:
                partition_index += 1
                swap(ls, pointer, partition_index)
        partition_index += 1
        swap(ls, h, partition_index)
        partition(ls, l, partition_index - 1)
        partition(ls, partition_index + 1, h)


# Main function
# Sorts an arbitrary list using the quicksort algorithm
# Returns a new list, sorted
def quicksort(ls: List):
    ls_copy = ls.copy()
    partition(ls_copy, 0, len(ls) - 1)
    return ls_copy
