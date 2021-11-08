from typing import List, Tuple
from .utils.morse_utils import Morse_Utils


class Word:
    def __init__(self, word: str, first_pos: Tuple[int, int]):
        self.__word: str = word.upper()
        self.__first_position: Tuple[int, int] = first_pos
        self.__all_positions: List[Tuple[int, int]] = [first_pos]
        self.__frequency: int = 1

    def size(self) -> int:
        return len(self.__word)

    def getWord(self) -> str:
        return self.__word

    def getFrequency(self) -> int:
        return self.__frequency

    def addInstance(self, instance_position: Tuple[int, int]) -> None:
        self.__all_positions.append(instance_position)
        self.__frequency += 1

    def getFirstPos(self) -> Tuple[int, int]:
        return self.__first_position

    def getDetails(self) -> str:
        return str(self)

    def __str__(self) -> str:
        details = ''
        details += Morse_Utils.encode_morse(self.__word)
        details += f'[{self.__word}] ({self.__frequency}) {self.__all_positions}\n'
        return details

    def __repr__(self) -> str:
        return self.__word