# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# Import Dependencies
from typing import List


def swap(ls, i, j):
    ls[j], ls[i] = ls[i], ls[j]


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


def quicksort(ls: List):
    ls_copy = ls.copy()
    partition(ls_copy, 0, len(ls) - 1)
    return ls_copy


if __name__ == "__main__":
    ls = [6, 4, 5, 6, 3, 5, 2, 4, 5]
    print(ls)
    print(quicksort(ls))
    print(ls)