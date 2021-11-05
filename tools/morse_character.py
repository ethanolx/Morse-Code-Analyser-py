from .data_structures.stack import Stack


class Morse_Character(Stack):
    def __init__(self, morse_char: str, pad_char: str = ' ', padding: int = 5):
        super().__init__()
        for symbol in morse_char:
            self.push(symbol)

        for i in range(padding - self.size()):
            self.push(pad_char)