# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# Class for an individual node in the Stack class
class Node:
    def __init__(self, val, next_node=None):
        # Value property is immutable after initialisation
        self.__value = val

        # Next node is not encapsulated
        self.next = next_node

    # Getter for value
    def get_value(self):
        return self.__value
