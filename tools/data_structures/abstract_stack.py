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
