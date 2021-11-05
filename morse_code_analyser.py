from typing import Dict, List, Set
from tools.morse_character import Morse_Character
from tools.sorting.quicksort import quicksort
from tools.utils.clear_console import clear_console
from tools.word import Word
from tools.utils.file_input import file_input


class Morse_Code_Analyser:
    def __init__(self, config=None):
        DEFAULT_CONFIG = {
            "author": {
                "name": "John Doe",
                "admin": "1234567",
                "class": "UNKNOWN",
                "module": "UNKNOWN",
            },
            "print_mode": "h",
        }

        CUSTOM_CONFIG = DEFAULT_CONFIG.copy()
        if config is not None:
            for k, v in config.items():
                CUSTOM_CONFIG[k] = v

        self.author: Dict[str, Dict[str, str]] = CUSTOM_CONFIG["author"]
        self.print_mode = CUSTOM_CONFIG["print_mode"]

    @staticmethod
    def multi_line_input():
        lines = []
        while True:
            line = input()
            if line:
                lines.append(line)
            else:
                break
        return "\n".join(lines)

    def print_morse_h(self, morse: str):
        print(morse)

    def print_morse_v(self, morse: str):
        lines = morse.splitlines()
        for line in lines:
            ls = []
            print_str = ''
            for char in line.split(sep=","):
                ls.append(Morse_Character(morse_char=char, pad_char=' ', padding=5))
            for _ in range(5):
                for char in ls:
                    print_str += char.pop()
                print_str += '\n'
            print(print_str)

    def run(self):
        choice = 0
        while choice < 4:
            clear_console()
            self.print_info()
            choice = self.get_choice()
            if choice == 1:
                self.change_printing_mode_1()
            elif choice == 2:
                print("Enter text to be converted:")
                lines = self.multi_line_input()
                morse = self.encode_morse_2(lines)
                if self.print_mode == "h":
                    self.print_morse_h(morse)
                else:
                    self.print_morse_v(morse)
            elif choice == 3:
                i_file = file_input('Enter input file:  ')
                o_file = file_input('Enter output file: ')
                self.analyse_morse_message_3(
                    input_file=i_file, output_file=o_file)
            elif choice == 4:
                print('Bye, thanks for using {}: Morse Code Analyser!'.format(self.author['module']))
            input('\nPress Enter to continue...')

    @staticmethod
    def simple_input(prompt: str):
        return input(prompt).strip().lower()

    @staticmethod
    def encode_morse_2(plain_text: str):
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
    def decode_morse_3(file: str):
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

    @staticmethod
    def get_stop_words(file: str = 'data/stopwords.txt'):
        with open(file=file, mode='r') as f:
            stop_words = {w.upper() for w in f.read().splitlines()}
        return stop_words

    @staticmethod
    def save_report(message: str, file: str):
        if file != '':
            with open(file=file, mode='w') as f:
                f.write(message)

    def analyse_morse_message_3(self, input_file: str, output_file: str):
        stop_words = self.get_stop_words()
        decoded_text = self.decode_morse_3(input_file)
        word_dict = self.get_frequencies(text=decoded_text)
        word_ls = list(word_dict.values())
        message_breakdown = self.get_message_breakdown(word_ls=word_ls)
        essential_message = self.get_essential_message(stop_words=stop_words, word_ls=word_ls)
        report = self.build_report(decoded_message=decoded_text, message_breakdown=message_breakdown, essential_message=essential_message)
        print(report)
        self.save_report(message=report, file=output_file)

    def get_message_breakdown(self, word_ls: List[Word]):
        sorted_words = quicksort(word_ls, key=lambda w: w.repr1())
        previous_frequency = sorted_words[0].getFrequency()
        message_breakdown = f'*** Morse words with frequency = {previous_frequency}\n'
        for word in sorted_words:
            current_frequency = word.getFrequency()
            if current_frequency < previous_frequency:
                if current_frequency == 1:
                    break
                message_breakdown += f'\n*** Morse words with frequency = {current_frequency}\n'
                previous_frequency = current_frequency
            message_breakdown += word.getDetails()
        return message_breakdown

    def get_essential_message(self, stop_words: Set[str], word_ls: List[Word]):
        sorted_words = quicksort(word_ls, key=lambda w: w.repr2())
        essential_message = ''
        for word in sorted_words:
            w = word.getWord()
            if w not in stop_words and w.isalpha():
                essential_message += w + ' '
        return essential_message

    def build_report(self, decoded_message: str, message_breakdown: str, essential_message: str):
        report = '*** Decoded morse text\n'
        report += decoded_message + '\n'
        report += message_breakdown + '\n'
        report += '*** Essential Message\n'
        report += essential_message + '\n'
        return report

    @staticmethod
    def get_frequencies(text: str):
        word_dict: Dict[str, Word] = {}
        for line_index, line in enumerate(text.splitlines()):
            for word_index, word in enumerate(line.split(sep=' ')):
                if word in word_dict:
                    word_dict[word].addInstance((line_index, word_index))
                else:
                    word_dict[word] = Word(word=word, first_pos=(line_index, word_index))
        return word_dict

    def print_info(self):
        print('*' * 57)
        print(
            f'''*\t{self.author['module']}: Morse Code Message Analyser\t*''')
        print('*' + '-' * 55 + '*')
        print('*\t\t\t\t\t\t\t*')
        print(f'''*\t- Done By: {self.author['name']}\t\t\t\t*''')
        print(f'''*\t- Class: {self.author['class']}\t\t\t\t*''')
        print('*\t\t\t\t\t\t\t*')
        print('*' * 57)

    @staticmethod
    def get_choice():
        print(
            "Please select your choice (1, 2, 3 or 4):\n \
            \t1.  Change printing mode\n \
            \t2.  Convert plain text to morse code\n \
            \t3.  Analyse morse code message\n \
            \t4.  Exit".expandtabs(tabsize=4)
        )
        try:
            choice = int(input("Enter your choice: "))
            assert 1 <= choice <= 4
        except Exception:
            print("Invalid input")
            return Morse_Code_Analyser.get_choice()
        return choice

    def change_printing_mode_1(self):
        mode = self.print_mode
        print(f"Current print mode is {mode}")
        while True:
            try:
                mode = self.simple_input(
                    f"Enter 'h' for horizontal or 'v' for vertical, then press enter: "
                )
                assert mode == "h" or mode == "v"
                break
            except Exception:
                print("Invalid input")
        self.print_mode = mode
        print(
            "The print mode has been changed to",
            "horizontal" if mode == "h" else "vertical",
        )


CONFIG = {
    "author": {
        "name": "Ethan Tan",
        "admin": "2012085",
        "class": "DAAA/2B/03",
        "module": "ST1507 DSAA",
    }
}

test = Morse_Code_Analyser(config=CONFIG)
test.run()
