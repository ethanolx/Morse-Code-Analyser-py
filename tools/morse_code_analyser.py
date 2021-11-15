from typing import Dict, List, Set, Tuple
from .data_structures.morse_character import Morse_Character
from .data_structures.message_breakdown_word import Message_Breakdown_Word
from .data_structures.essential_message_word import Essential_Message_Word
from .sorting.quicksort import quicksort
from .utils.io_utils import simple_input, multi_line_input, file_input, clear_console
from .utils.morse_utils import Morse_Utils
from os.path import exists, isfile


class Morse_Code_Analyser:
    def __init__(self, config=None):
        self.load_config(config=config)

    def load_config(self, config=None):
        DEFAULT_CONFIG = {
            'author': {
                'name': 'John Doe',
                'admin': '1234567',
                'class': 'UNKNOWN',
                'module': 'UNKNOWN',
            },
            '__print_mode': 'h',
            'stopwords_file': 'data/stopwords.txt',
            'min_significant_frequency': 2
        }

        CUSTOM_CONFIG = DEFAULT_CONFIG.copy()
        if config is not None:
            for k, v in config.items():
                CUSTOM_CONFIG[k] = v

        self.__author: Dict[str, Dict[str, str]] = CUSTOM_CONFIG['author']
        self.__print_mode = CUSTOM_CONFIG['__print_mode']
        self.__min_significant_frequency = CUSTOM_CONFIG['min_significant_frequency']
        self.set_stop_words(file=CUSTOM_CONFIG['stopwords_file'])

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
                break
            input('\nPress Enter to continue...')

    def change_printing_mode_1(self):
        mode = self.__print_mode
        modes = {
            'h': 'horizontal',
            'v': 'vertical'
        }
        print(f'Current print mode is {mode}')
        while True:
            try:
                mode = simple_input(
                    f'Enter \'h\' for horizontal or \'v\' for vertical, then press enter: ')
                assert mode == 'h' or mode == 'v' or mode == ''
                break
            except Exception:
                print('Invalid input')
        if mode != '':
            self.__print_mode = mode
            print('The print mode has been changed to', modes[mode])
        else:
            print('Operation cancelled by user. The print mode remains as',
                  modes[self.__print_mode])

    def convert_text_to_morse_2(self):
        print('Enter text to be converted:')
        lines = multi_line_input()
        morse = Morse_Utils.encode_morse(lines)
        if self.__print_mode == 'h':
            self.print_morse_h(morse)
        else:
            self.print_morse_v(morse)

    def analyse_morse_message_3(self):
        input_file, output_file = self.get_target_files()
        try:
            decoded_text = self.get_decoded_message(input_file=input_file)
            message_breakdown_ls, essential_message_ls = self.get_frequencies(
                text=decoded_text)
            message_breakdown = self.get_message_breakdown(
                word_ls=message_breakdown_ls)
            essential_message = self.get_essential_message(
                stop_words=self.__stop_words, word_ls=essential_message_ls)
            report = self.build_report(
                decoded_message=decoded_text, message_breakdown=message_breakdown, essential_message=essential_message)
            print('\n', report, sep='')
            self.save_report(message=report, file=output_file)
        except AssertionError as err:
            print(err, 'Aborting...')

    def exit_4(self):
        print('Bye, thanks for using {}: Morse Code Analyser!'.format(
            self.__author['module']))

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
            for char in line.split(sep=','):
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

    def get_target_files(self):
        return self.get_input_file(), self.get_output_file()

    def get_input_file(self):
        try:
            input_file = file_input('Enter input file:  ')
            assert exists(input_file), 'Invalid input file'
            assert isfile(input_file), 'Not a file'
            return input_file
        except AssertionError as err:
            print(err)
            return self.get_input_file()

    def get_output_file(self):
        try:
            output_file = file_input('Enter output file: ')
            assert output_file == '' or (exists(
                output_file) and isfile(output_file)), 'Invalid output file'
            return output_file
        except AssertionError as err:
            print(err)
            return self.get_output_file()

    def get_frequencies(self, text: str):
        word_dict: Dict[str, Tuple[Message_Breakdown_Word,
                                   Essential_Message_Word]] = {}
        for line_index, line in enumerate(text.splitlines()):
            for word_index, word in enumerate(line.split(sep=' ')):
                if word in word_dict:
                    word_dict[word][0].addInstance((line_index, word_index))
                    word_dict[word][1].addInstance()
                else:
                    word_dict[word] = (
                        Message_Breakdown_Word(
                            word=word, first_pos=(line_index, word_index)),
                        Essential_Message_Word(
                            word=word, first_pos=(line_index, word_index))
                    )
        message_breakdown_word_list = []
        essential_message_word_list = []
        for mbw, emw in word_dict.values():
            message_breakdown_word_list.append(mbw)
            essential_message_word_list.append(emw)
        return message_breakdown_word_list, essential_message_word_list

    def get_decoded_message(self, input_file: str):
        decoded_message = Morse_Utils.decode_morse(input_file)
        return decoded_message

    def get_message_breakdown(self, word_ls: List[Essential_Message_Word]):
        sorted_words: List[Essential_Message_Word] = quicksort(
            word_ls)  # type: ignore
        try:
            previous_frequency = sorted_words[0].getFrequency()
        except IndexError:
            previous_frequency = self.__min_significant_frequency - 1
        message_breakdown = ''
        if previous_frequency >= self.__min_significant_frequency:
            message_breakdown += f'*** Morse words with frequency = {previous_frequency}\n'
        for word in sorted_words:
            current_frequency = word.getFrequency()
            if current_frequency < self.__min_significant_frequency:
                break
            if current_frequency < previous_frequency:
                message_breakdown += f'\n*** Morse words with frequency = {current_frequency}\n'
                previous_frequency = current_frequency
            message_breakdown += word.getDetails()
        return message_breakdown

    def get_essential_message(self, stop_words: Set[str], word_ls: List[Message_Breakdown_Word]):
        sorted_words: List[Message_Breakdown_Word] = quicksort(
            word_ls)  # type: ignore
        essential_message = ''
        for word in sorted_words:
            w = word.getWord()
            if w not in stop_words and w.isalpha():
                essential_message += w + ' '
        return essential_message

    def build_report(self, decoded_message: str, message_breakdown: str, essential_message: str):
        report = '*** Decoded morse text\n' + decoded_message + '\n' \
            if decoded_message != '' \
            else '*** No decoded morse text\n'
        report += message_breakdown + '\n' \
            if message_breakdown != '' \
            else f'*** No morse words with frequency >= {self.__min_significant_frequency}\n'
        report += '*** Essential Message\n' + essential_message \
            if essential_message != '' \
            else '*** No essential message'
        return report

    def save_report(self, message: str, file: str):
        if file != '':
            with open(file=file, mode='w') as f:
                f.write(message)

    # Generic Utility Methods
    def get_choice(self):
        print(
            'Please select your choice (1, 2, 3 or 4):\n \
            \t1.  Change printing mode\n \
            \t2.  Convert plain text to morse code\n \
            \t3.  Analyse morse code message\n \
            \t4.  Exit'.expandtabs(tabsize=4)
        )
        try:
            choice = int(input('Enter your choice: '))
            assert 1 <= choice <= 4
        except Exception:
            print('Invalid input')
            return self.get_choice()
        return choice

    def print_info(self):
        print('*' * 57)
        print(
            f'''*\t{self.__author['module']}: Morse Code Message Analyser\t*''')
        print('*' + '-' * 55 + '*')
        print('*\t\t\t\t\t\t\t*')
        print(f'''*\t- Done By: {self.__author['name']}\t\t\t\t*''')
        print(f'''*\t- Class: {self.__author['class']}\t\t\t\t*''')
        print('*\t\t\t\t\t\t\t*')
        print('*' * 57)
