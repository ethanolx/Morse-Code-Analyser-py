from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

def file_input(message: str):
    return prompt(
        message=message,
        history=FileHistory("./tmp/history.txt"),
        auto_suggest=AutoSuggestFromHistory()
    )