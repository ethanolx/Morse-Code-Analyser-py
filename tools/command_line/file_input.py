from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory

user_input = prompt(
    message="> ",
    history=FileHistory("./tmp/history.txt"),
    auto_suggest=AutoSuggestFromHistory()
)