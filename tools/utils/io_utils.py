from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
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
    return prompt(
        message=message,
        history=FileHistory("./tmp/history.txt"),
        auto_suggest=AutoSuggestFromHistory()
    )
