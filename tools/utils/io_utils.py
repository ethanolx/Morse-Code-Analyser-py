# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# Import Dependencies
import os
import re


# Clears console, imitates reloading the screen
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


# Removes all internal whitespace
def whitespace_reducer(text: str):
    return re.sub(pattern='[\\s]+', repl=' ', string=text)


# Converts non alphanumeric characters to whitespace
def strip_special_characters(text: str):
    return re.sub(pattern='[^A-Za-z0-9]', repl=' ', string=text)

# Retrieves formatted multi-line input
def multi_line_input():
    lines = []
    while True:
        line = input()
        if line:
            lines.append(whitespace_reducer(line))
        else:
            break
    return "\n".join(lines)


# Retrieves formatted input
def simple_input(prompt: str):
    return whitespace_reducer(input(prompt)).strip().lower()


# Retrieves formatted file path input
def file_input(message: str):
    return whitespace_reducer(input(message)).strip()
