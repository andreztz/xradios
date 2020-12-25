from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.completion import WordCompleter

from xradios.tui.constants import PROMPT_BUFFER


COMMANDS = [
    "play",
    "pause",
    "stop",
    "rec",
    "info",
    "help",
    "list",
    "bytag",
    "bycodec",
    "bycountry",
    "bylanguage",
    "byname",
    "bystate",
    "byuuid",
    "tags",
    "exit",
    "search",
    "nowplaying",
]


completer = WordCompleter(COMMANDS, ignore_case=True)


class PromptBuffer(Buffer):
    def __init__(self, *args, **kwargs):
        super().__init__(
            completer=completer,
            complete_while_typing=True,
            name=PROMPT_BUFFER
        )


buffer = PromptBuffer()
