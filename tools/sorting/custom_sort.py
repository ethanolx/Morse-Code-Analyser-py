from typing import Callable, List


def custom_sort_key(ls: List, key: Callable):
    return [(el, key(el)) for el in ls]