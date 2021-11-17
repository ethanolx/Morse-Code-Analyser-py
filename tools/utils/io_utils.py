# Name:     Ethan Tan
# Admin:    P2012085
# Class:    DAAA/2B/03

# Import Dependencies
import os
import re


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def whitespace_reducer(text: str):
    return re.sub(pattern='[\\s]+', repl=' ', string=text)


def multi_line_input():
    lines = []
    while True:
        line = input()
        if line:
            lines.append(whitespace_reducer(line))
        else:
            break
    return "\n".join(lines)


def simple_input(prompt: str):
    return whitespace_reducer(input(prompt)).strip().lower()


def file_input(message: str):
    return whitespace_reducer(input(message)).strip()
