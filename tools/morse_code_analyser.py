# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# Import Dependencies
from typing import Dict, List, Literal, Set, Tuple, Union
from .data_structures.morse_character import Morse_Character
from .data_structures.message_breakdown_word import Message_Breakdown_Word
from .data_structures.essential_message_word import Essential_Message_Word
from .sorting.quicksort import quicksort
from .utils.io_utils import strip_special_characters, simple_input, multi_line_input, file_input, clear_console
from .utils.morse_utils import Morse_Utils
from os.path import exists, isfile


# Main object
class Morse_Code_Analyser:
    def __init__(self, config=None):
        self.__load_config(config=config)

    # Load custom configuration options
    def __load_config(self, config=None):
        DEFAULT_CONFIG = {
            'author': {
                'name': 'John Doe',
                'admin': '1234567',
                'class': 'UNKNOWN',
                'module': 'UNKNOWN',
            },
            'print_mode': 'h',
            'stopwords_file': 'data/stopwords.txt',
            'min_significant_frequency': 1
        }

        # Defaults to default configuration if key is not specified in config
        CUSTOM_CONFIG = DEFAULT_CONFIG.copy()
        if config is not None:
            for k, v in config.items():
                CUSTOM_CONFIG[k] = v

        # Details to be displayed
        self.__author: Dict[str, Dict[str, str]] = CUSTOM_CONFIG['author']

        # Default printing mode
        self.__print_mode: Union[Literal['h'],
                                 Literal['v']] = CUSTOM_CONFIG['print_mode']

        # Minimum lowest frequency to display in the get_message_breakdown method in Option 3
        self.__min_significant_frequency: int = CUSTOM_CONFIG['min_significant_frequency']

        # Relative path to file containing stop words
        self.__set_stop_words(file=CUSTOM_CONFIG['stopwords_file'])

    # Operational Methods
    # Runs the program
    def run(self):
        choice = 0
        while choice < 4:
            clear_console()

            # Displays the author's information
            self.__print_info()

            # Get the user's choice
            choice = self.__get_choice()

            if choice == 1:
                self.__change_printing_mode_1()
            elif choice == 2:
                self.__convert_text_to_morse_2()
            elif choice == 3:
                self.__analyse_morse_message_3()
            elif choice == 4:
                self.__exit_4()
                break
            input('\nPress Enter to continue...')

    # Allows the user to change the printing mode for Option 2
    # Empty input will return to the menu without changing the printing mode
    def __change_printing_mode_1(self):
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

    # Converts a (multi-line) message in plain text to morse code and prints it out
    #   based on the current printing mode
    def __convert_text_to_morse_2(self):
        print('Enter text to be converted:')
        lines = multi_line_input()
        morse = Morse_Utils.encode_morse(lines)
        if self.__print_mode == 'h':
            self.__print_morse_h(morse)
        else:
            self.__print_morse_v(morse)

    # Converts a morse code message in a file to plain text
    # Displays a breakdown of the frequencies of each word in the message
    # Displays the essential message, with stop words removed
    def __analyse_morse_message_3(self):
        input_file, output_file = self.__get_target_files()
        try:
            decoded_text = self.__get_decoded_message(input_file=input_file)
            stripped_decoded_text = strip_special_characters(decoded_text)
            message_breakdown_ls, essential_message_ls = self.__get_frequencies(
                text=stripped_decoded_text)
            message_breakdown = self.__get_message_breakdown(
                word_ls=message_breakdown_ls)
            essential_message = self.__get_essential_message(
                stop_words=self.__stop_words, word_ls=essential_message_ls)
            report = self.__build_report(
                decoded_message=decoded_text, message_breakdown=message_breakdown, essential_message=essential_message)
            print('\n', report, sep='')
            self.__save_report(message=report, file=output_file)
        except AssertionError as err:
            print(err, 'Aborting...')

    # Displays a friendly farewell message
    def __exit_4(self):
        print('Bye, thanks for using {}: Morse Code Analyser!'.format(
            self.__author['module']))

    # Utility Methods

    # Option 2

    # Prints the encoded string horizontally
    @staticmethod
    def __print_morse_h(morse: str):
        print(morse)

    # Prints the encoded string vertically
    @staticmethod
    def __print_morse_v(morse: str):
        lines = morse.splitlines()
        for line in lines:
            ls = []
            # A list is used to collect the characters as
            #   repeated appending has an amortized worst case time complexity of O(n) whereas
            #   repeated string concatenation has a time complexity of O(n^2)
            print_ls = []
            for char in line.split(sep=','):
                ls.append(Morse_Character(
                    morse_char=char, pad_char=' ', padding=5))

            # Each morse character has a maximum length of 5
            for _ in range(5):
                for char in ls:
                    print_ls.append(char.pop())
                print_ls.append('\n')
            print(''.join(print_ls))

    # Option 3

    # Loads the stop words from the file specified
    def __set_stop_words(self, file: str):
        with open(file=file, mode='r') as f:
            stop_words = {w.upper() for w in f.read().splitlines()}
        self.__stop_words = stop_words

    # Returns the input and output files
    def __get_target_files(self):
        return self.__get_input_file(), self.__get_output_file()

    # Tries recursively to obtain a valid input file from the user
    def __get_input_file(self):
        try:
            input_file = file_input('Enter input file:  ')
            assert exists(input_file), 'Invalid input file'
            assert isfile(input_file), 'Not a file'
            return input_file
        except AssertionError as err:
            print(err)
            return self.__get_input_file()

    # Tries recursively to obtain a valid output file from the user
    # Empty input will cause report to not be saved
    def __get_output_file(self):
        try:
            output_file = file_input('Enter output file: ')
            if output_file == '':
                return ''
            with open(file=output_file, mode='w') as f:
                f.write('')
            return output_file
        except FileNotFoundError:
            print('Invalid output file name')
            return self.__get_output_file()

    # Decodes morse code message from input file
    def __get_decoded_message(self, input_file: str):
        decoded_message = Morse_Utils.decode_morse(input_file)
        return decoded_message

    # Returns a list of words to be used by __get_message_breakdown and __get_essential_message methods
    def __get_frequencies(self, text: str):
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

    # Analyses frequencies and positions of the words in the morse code message
    def __get_message_breakdown(self, word_ls: List[Message_Breakdown_Word]):
        sorted_words: List[Message_Breakdown_Word] = quicksort(
            word_ls)
        try:
            previous_frequency = sorted_words[0].getFrequency()
        except IndexError:
            previous_frequency = self.__min_significant_frequency - 1
        message_breakdown = []
        if previous_frequency >= self.__min_significant_frequency:
            message_breakdown.append(
                f'*** Morse words with frequency = {previous_frequency}\n')
        for word in sorted_words:
            current_frequency = word.getFrequency()
            if current_frequency < self.__min_significant_frequency:
                break
            if current_frequency < previous_frequency:
                message_breakdown.append(
                    f'\n*** Morse words with frequency = {current_frequency}\n')
                previous_frequency = current_frequency
            message_breakdown.append(word.getDetails())
        return ''.join(message_breakdown)

    # Analyses essential message through sorting by frequency and first position of the words
    def __get_essential_message(self, stop_words: Set[str], word_ls: List[Essential_Message_Word]):
        sorted_words: List[Essential_Message_Word] = quicksort(
            word_ls)  # type: ignore
        essential_message = []
        for word in sorted_words:
            w = word.getWord()
            if w not in stop_words and w.isalpha():
                essential_message.append(w)
        return ' '.join(essential_message)

    # Builds report from the three components
    def __build_report(self, decoded_message: str, message_breakdown: str, essential_message: str):
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

    # Saves report to the output file, if specified
    def __save_report(self, message: str, file: str):
        if file != '':
            with open(file=file, mode='w') as f:
                f.write(message)

    # Generic Utility Methods

    # Retrieves valid option from user, recursively
    def __get_choice(self):
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
            return self.__get_choice()
        return choice

    # Prints the author's details
    def __print_info(self):
        print('*' * 57)
        print(
            f'''*\t{self.__author['module']}: Morse Code Message Analyser\t*''')
        print('*' + '-' * 55 + '*')
        print('*\t\t\t\t\t\t\t*')
        print(f'''*\t- Done By: {self.__author['name']}\t\t\t\t*''')
        print(f'''*\t- Class: {self.__author['class']}\t\t\t\t*''')
        print('*\t\t\t\t\t\t\t*')
        print('*' * 57)
