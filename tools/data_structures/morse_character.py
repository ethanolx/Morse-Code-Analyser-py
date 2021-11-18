# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# Import Dependencies
from .stack import Stack


# Models a morse character for vertical printing
class Morse_Character(Stack):
    def __init__(self, morse_char: str, pad_char: str = ' ', padding: int = 5):
        super().__init__()

        # Pads all characters to length 5, as longest morse character is 5,
        #   thus enforcing O(1) time complexity
        for symbol in morse_char:
            self.push(symbol)

        for _ in range(padding - self.size()):
            self.push(pad_char)
