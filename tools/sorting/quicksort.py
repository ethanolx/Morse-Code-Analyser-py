from typing import Callable, List
from .custom_sort import custom_sort_key


def swap(ls, i, j):
    ls[j], ls[i] = ls[i], ls[j]


def partition(ls, l, h, key: bool = False):
    if l < h:
        partition_index = pointer = l - 1
        partition_num = ls[h]
        if key:
            partition_num = partition_num[1]
        for el in ls[l:h]:
            pointer += 1
            if key:
                el = el[1]
            if el < partition_num:
                partition_index += 1
                swap(ls, pointer, partition_index)
        partition_index += 1
        swap(ls, h, partition_index)
        partition(ls, l, partition_index - 1)
        partition(ls, partition_index + 1, h)


def quicksort(ls: List, key: Callable = None):
    ls_copy = ls.copy() if key is None else custom_sort_key(ls, key)
    activate_key = key is not None
    partition(ls_copy, 0, len(ls) - 1, key=activate_key)
    return [el for el, _ in ls_copy]


if __name__ == "__main__":
    ls = [6, 4, 5, 6, 3, 5, 2, 4, 5]
    print(ls)
    print(quicksort(ls, key=lambda w: -len(w)))
    print(ls)