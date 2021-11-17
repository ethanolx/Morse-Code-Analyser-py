# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# Import Dependencies
from typing import Tuple
from .word import Word


class Essential_Message_Word(Word):
    def __init__(self, word: str, first_pos: Tuple[int, int]):
        super().__init__(word=word)
        self.__first_position: Tuple[int, int] = first_pos

    def addInstance(self) -> None:
        self._frequency += 1

    def getFirstPos(self) -> Tuple[int, int]:
        return self.__first_position

    def __lt__(self, otherWord) -> bool:
        return (-self.getFrequency(), self.getFirstPos()) < (-otherWord.getFrequency(), otherWord.getFirstPos())
