# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# Import Dependencies
from abc import ABC, abstractmethod


class Abstract_Stack(ABC):
    @abstractmethod
    def push():
        pass

    @abstractmethod
    def peek():
        pass

    @abstractmethod
    def pop():
        pass

    @abstractmethod
    def empty():
        pass

    @abstractmethod
    def size():
        pass
