from typing import Dict, List, Set, Tuple
from tools.data_structures.stack import Stack
from tools.sorting.custom_sort import custom_sort_key
from tools.sorting.quicksort import quicksort

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

        self.author = CUSTOM_CONFIG["author"]
        self.print_mode = CUSTOM_CONFIG["print_mode"]
        self.print_info()

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
                ls.append(self.pad_morse(morse=char, char=" "))
            for _ in range(5):
                for char in ls:
                    print_str += char.pop()
                print_str += '\n'
            print(print_str)

    @staticmethod
    def pad_morse(morse: str, char: str, length: int = 5):
        return Stack.from_list(list(morse + ((length - len(morse)) * char)))

    def run(self):
        # self.print_info()
        choice = 0
        while choice < 4:
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
                i_file = self.simple_input('Enter input file:')
                o_file = self.simple_input('Enter output file:')
                self.analyse_morse_message_3(input_file=i_file, output_file=o_file)

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

    def analyse_morse_message_3(self, input_file: str, output_file: str):
        stop_words = ''
        with open('data/stopwords.txt', 'r') as f:
            stop_words = set([w.upper() for w in f.read().splitlines()])
        report = '*** Decoded morse text\n'
        text = self.decode_morse_3(input_file)
        report += text + '\n'
        freq_word_dict, word_loc_dict = self.get_frequencies(text)
        unique_freqs = set(freq_word_dict.keys())
        # print(freq_word_dict)
        essential_message = []
        while unique_freqs:
            highest_freq = max(unique_freqs)
            report += f'*** Morse words with frequency = {highest_freq}\n'
            word_list = self.sort_words(freq_word_dict[highest_freq])
            tmp_essential_message = []
            for word in word_list:
                if word not in stop_words:
                    tmp_essential_message.append(word)
                report += self.encode_morse_2(word)
                report += f'[{word}] ({highest_freq}) {word_loc_dict[word]}\n'
            essential_message.extend(quicksort(tmp_essential_message, key=lambda w: word_loc_dict[w][0]))
            unique_freqs.remove(highest_freq)
            report += '\n'
        report += '*** Essential Message\n'
        report += ' '.join(essential_message)
        print(report)
        self.save_report(message=report, file=output_file)

    @staticmethod
    def save_report(message: str, file: str):
        if file != '':
            with open(file=file, mode='w') as f:
                f.write(message)

    @staticmethod
    def get_frequencies(text: str):
        import re
        word_freq_dict: Dict[str, int] = {}
        word_loc_dict: Dict[str, List[Tuple[int, int]]] = {}
        line_index = 0
        for line in text.splitlines():
            word_index = 0
            for word in line.split(sep=' '):
                # if len(word) > 0:
                if word in word_freq_dict.keys():
                    word_freq_dict[word] += 1
                    word_loc_dict[word].append((line_index, word_index))
                else:
                    word_freq_dict[word] = 1
                    word_loc_dict[word] = [(line_index, word_index)]
                word_index += 1
            line_index += 1
        freqs_set = set(v for k, v in word_freq_dict.items())
        word_freq_dict_aug = set(k + ':' + str(v) for k, v in word_freq_dict.items())
        freq_word_dict: Dict[int, Set[str]] = {fr: set() for fr in freqs_set}
        for word_freq in word_freq_dict_aug:
            w, f = word_freq.split(':')
            freq_word_dict[int(f)].add(w)
        return freq_word_dict, word_loc_dict

    @staticmethod
    def sort_words(words: Set[str]):
        return quicksort(list(words), key=lambda w: (len(w), w))

    def print_info(self):
        print('*' * 57)
        print(f'''*\t{self.author['module']}: Morse Code Message Analyser\t*''')
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
        while True:
            try:
                choice = int(input("Enter your choice: "))
                assert 1 <= choice <= 4
                break
            except Exception:
                print("Invalid input")
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
