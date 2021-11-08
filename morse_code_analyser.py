from typing import Dict, List, Set
from tools.morse_character import Morse_Character
from tools.sorting.quicksort import quicksort
from tools.word import Word
from tools.utils.io_utils import simple_input, multi_line_input, file_input, clear_console
from tools.utils.morse_utils import Morse_Utils


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
            "stopwords_file": "data/stopwords.txt"
        }

        CUSTOM_CONFIG = DEFAULT_CONFIG.copy()
        if config is not None:
            for k, v in config.items():
                CUSTOM_CONFIG[k] = v

        self.author: Dict[str, Dict[str, str]] = CUSTOM_CONFIG["author"]
        self.print_mode = CUSTOM_CONFIG["print_mode"]
        self.set_stop_words(file=CUSTOM_CONFIG["stopwords_file"])

    # Operational Methods
    def run(self):
        choice = 0
        while choice < 4:
            clear_console()
            self.print_info()
            choice = self.get_choice()
            if choice == 1:
                self.change_printing_mode_1()
            elif choice == 2:
                self.convert_text_to_morse_2()
            elif choice == 3:
                self.analyse_morse_message_3()
            elif choice == 4:
                self.exit_4()
            input('\nPress Enter to continue...')

    def change_printing_mode_1(self):
        mode = self.print_mode
        print(f"Current print mode is {mode}")
        while True:
            try:
                mode = simple_input(
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

    def convert_text_to_morse_2(self):
        print("Enter text to be converted:")
        lines = multi_line_input()
        morse = Morse_Utils.encode_morse(lines)
        if self.print_mode == "h":
            self.print_morse_h(morse)
        else:
            self.print_morse_v(morse)

    def analyse_morse_message_3(self):
        input_file = file_input('Enter input file:  ')
        output_file = file_input('Enter output file: ')
        decoded_text = Morse_Utils.decode_morse(input_file)
        word_dict = self.get_frequencies(text=decoded_text)
        word_ls = list(word_dict.values())
        message_breakdown = self.get_message_breakdown(word_ls=word_ls)
        essential_message = self.get_essential_message(
            stop_words=self.__stop_words, word_ls=word_ls)
        report = self.build_report(
            decoded_message=decoded_text, message_breakdown=message_breakdown, essential_message=essential_message)
        print(report)
        self.save_report(message=report, file=output_file)

    def exit_4(self):
        print('Bye, thanks for using {}: Morse Code Analyser!'.format(
            self.author['module']))

    # Utility Methods
    # Option 1
    @staticmethod
    def print_morse_h(morse: str):
        print(morse)

    @staticmethod
    def print_morse_v(morse: str):
        lines = morse.splitlines()
        for line in lines:
            ls = []
            print_str = ''
            for char in line.split(sep=","):
                ls.append(Morse_Character(
                    morse_char=char, pad_char=' ', padding=5))
            for _ in range(5):
                for char in ls:
                    print_str += char.pop()
                print_str += '\n'
            print(print_str)

    # Option 3
    def set_stop_words(self, file: str):
        with open(file=file, mode='r') as f:
            stop_words = {w.upper() for w in f.read().splitlines()}
        self.__stop_words = stop_words

    def get_frequencies(self, text: str):
        word_dict: Dict[str, Word] = {}
        for line_index, line in enumerate(text.splitlines()):
            for word_index, word in enumerate(line.split(sep=' ')):
                if word in word_dict:
                    word_dict[word].addInstance((line_index, word_index))
                else:
                    word_dict[word] = Word(
                        word=word, first_pos=(line_index, word_index))
        return word_dict

    def get_message_breakdown(self, word_ls: List[Word]):
        sorted_words = quicksort(
            word_ls, key=lambda w: (-w.getFrequency(), w.size(), w.getWord()))
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
        sorted_words = quicksort(
            word_ls, key=lambda w: (-w.getFrequency(), w.getFirstPos()))
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

    def save_report(self, message: str, file: str):
        if file != '':
            with open(file=file, mode='w') as f:
                f.write(message)

    # Generic Utility Methods
    def get_choice(self):
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
            return self.get_choice()
        return choice

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


if __name__ == '__main__':
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
