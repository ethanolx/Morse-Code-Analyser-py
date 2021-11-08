from abc import ABC, abstractmethod


class Morse_Utils(ABC):
    @abstractmethod
    def __init__(self):
        pass

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
        morse = ""
        encoded_chars = TEXT_TO_MORSE.keys()
        contents = plain_text.upper().splitlines()
        for line in contents:
            for char in list(line):
                morse += TEXT_TO_MORSE[char] if char in encoded_chars else char
                morse += ","
            morse = morse[:-1] + "\n"
        return morse

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
        text = ""
        with open(file=file) as f:
            contents = f.read().splitlines()
            for line in contents:
                for char in line.split(","):
                    text += MORSE_TO_TEXT[char] if "." in char or "-" in char else char
                text += "\n"
        return text
