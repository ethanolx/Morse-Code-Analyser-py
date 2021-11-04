from abc import ABC


class Morse_Utils(ABC):
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
