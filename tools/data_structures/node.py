# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

class Node:
    def __init__(self, val, next_node=None):
        self.__value = val
        self.attach_next(next_node)

    def get_value(self):
        return self.__value

    def attach_next(self, next_node):
        self.__next = next_node

    def get_next(self):
        return self.__next
