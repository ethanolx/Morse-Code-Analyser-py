# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# Import Dependencies
from abc import ABC, abstractmethod


class Word(ABC):
    def __init__(self, word: str):
        self._word: str = word.upper()
        self._frequency: int = 1

    def size(self) -> int:
        return len(self._word)

    def getWord(self) -> str:
        return self._word

    def getFrequency(self) -> int:
        return self._frequency

    @abstractmethod
    def addInstance(self):
        pass

    @abstractmethod
    def __lt__(self, otherWord):
        pass
