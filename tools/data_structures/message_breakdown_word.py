# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# Import Dependencies
from typing import List, Tuple
from .word import Word
from ..utils.morse_utils import Morse_Utils


# Model for a word in the message breakdown
class Message_Breakdown_Word(Word):
    def __init__(self, word: str, first_pos: Tuple[int, int]):
        super().__init__(word=word)
        self.__all_positions: List[Tuple[int, int]] = [first_pos]

    def addInstance(self, instance_position: Tuple[int, int]) -> None:
        self.__all_positions.append(instance_position)
        self._frequency += 1

    def getDetails(self) -> str:
        details = ''
        details += Morse_Utils.encode_morse(self._word)
        details += f'[{self._word}] ({self._frequency}) {self.__all_positions}\n'
        return details

    def __lt__(self, otherWord) -> bool:
        return (-self.getFrequency(), self.size(), self.getWord()) < (-otherWord.getFrequency(), otherWord.size(), otherWord.getWord())
