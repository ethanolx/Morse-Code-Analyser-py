from typing import List
from .abstract_stack import Abstract_Stack
from .node import Node


class Stack(Abstract_Stack):
    def __init__(self):
        self.__head = None
        self.__size = 0

    def push(self, val):
        new_node = Node(val=val)
        if self.__head is None:
            self.__head = new_node
        else:
            new_node.attach_next(next_node=self.__head)
            self.__head = new_node
        self.__size += 1

    def peek(self):
        if self.__head is not None:
            return self.__head.get_value()
        else:
            return None

    def pop(self):
        tmp_val = None
        if self.__head is not None:
            tmp_val = self.__head.get_value()
            self.__head = self.__head.get_next()
            self.__size -= 1
        return tmp_val

    def __len__(self) -> int:
        return self.__size

    def __add__(self, val):
        self.push(val=val)

    def __subtract__(self):
        return self.pop()

    def __repr__(self):
        def print_node_rec(node: Node):
            full_stack = ""
            if node is not None:
                full_stack += str(node.get_value()) + " "
                full_stack += print_node_rec(node.get_next())
            return full_stack

        return print_node_rec(self.__head)  # type: ignore

    def empty(self):
        self.__size = 0
        self.__head = None

    @staticmethod
    def from_list(ls: List):
        new_stack = Stack()
        for el in ls:
            new_stack.push(el)
        return new_stack
