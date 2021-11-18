# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# Import Dependencies
from abc import ABC, abstractmethod


# Merely a namespace for morse-to-text translation functions
class Morse_Utils(ABC):
    @abstractmethod
    def __init__(self):
        pass

    # Encodes plain text to morse code
    @staticmethod
    def encode_morse(plain_text: str):
        TEXT_TO_MORSE = {
            "A": ".-",
            "B": "-...",
            "C": "-.-.",
            "D": "-..",
            "E": ".",
            "F": "..-.",
            "G": "--.",
            "H": "....",
            "I": "..",
            "J": ".---",
            "K": "-.-",
            "L": ".-..",
            "M": "--",
            "N": "-.",
            "O": "---",
            "P": ".--.",
            "Q": "--.-",
            "R": ".-.",
            "S": "...",
            "T": "-",
            "U": "..-",
            "V": "...-",
            "W": ".--",
            "X": "-..-",
            "Y": "-.--",
            "Z": "--..",
            "1": ".----",
            "2": "..---",
            "3": "...--",
            "4": "....-",
            "5": ".....",
            "6": "-....",
            "7": "--...",
            "8": "---..",
            "9": "----.",
            "0": "-----",
        }
        morse_ls = []
        contents = plain_text.upper().splitlines()
        for line in contents:
            for char in line:
                morse_ls.append(
                    TEXT_TO_MORSE[char] if char in TEXT_TO_MORSE else char)
                morse_ls.append(",")
            morse_ls.pop()
            morse_ls.append('\n')
        return ''.join(morse_ls)

    # Decodes morse code to plain text
    @staticmethod
    def decode_morse(file: str):
        MORSE_TO_TEXT = {
            ".-": "A",
            "-...": "B",
            "-.-.": "C",
            "-..": "D",
            ".": "E",
            "..-.": "F",
            "--.": "G",
            "....": "H",
            "..": "I",
            ".---": "J",
            "-.-": "K",
            ".-..": "L",
            "--": "M",
            "-.": "N",
            "---": "O",
            ".--.": "P",
            "--.-": "Q",
            ".-.": "R",
            "...": "S",
            "-": "T",
            "..-": "U",
            "...-": "V",
            ".--": "W",
            "-..-": "X",
            "-.--": "Y",
            "--..": "Z",
            ".----": "1",
            "..---": "2",
            "...--": "3",
            "....-": "4",
            ".....": "5",
            "-....": "6",
            "--...": "7",
            "---..": "8",
            "----.": "9",
            "-----": "0",
        }
        try:
            with open(file=file) as f:
                contents = f.read().splitlines()
                text_ls = []
                for line in contents:
                    for char in line.split(","):
                        text_ls += MORSE_TO_TEXT[char] if "." in char or "-" in char else char
                    text_ls.append("\n")
            return "".join(text_ls)
        except KeyError:
            raise AssertionError(
                f'Morse code in file {file} is in invalid format.')
