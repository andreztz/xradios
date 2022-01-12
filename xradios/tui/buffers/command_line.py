from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.completion import WordCompleter

from xradios.tui.constants import COMMAND_LINE_BUFFER


COMMANDS = [
    "play",
    "stop",
    "tags",
    "exit",
    "search",
    "name=",
    "name_exact=",
    "country=",
    "country_exact=",
    "countrycode=",
    "state=",
    "state_exact=",
    "language=",
    "language_exact=",
    "tag=",
    "tag_exact=",
    "bitrate_min=",
    "bitrate_max=",
    "has_geo_info=",
    "has_extended_info=",
    "is_https=",
    "order=",
    "reverse=",
    "limit=",
    "hidebroken=",
    "favorite-add",
    "favorite-rm",
]


completer = WordCompleter(COMMANDS, ignore_case=True)


class CommandLineBuffer(Buffer):
    def __init__(self, *args, **kwargs):
        super().__init__(
            completer=completer,
            complete_while_typing=True,
            name=COMMAND_LINE_BUFFER
        )


buffer = CommandLineBuffer()
