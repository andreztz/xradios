from prompt_toolkit.layout import BufferControl
from prompt_toolkit.widgets import Frame
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.layout.containers import ScrollOffsets
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers import MarkdownLexer


class PopupWindow:
    def __init__(self, buffer, title):
        self._title = title
        self._buffer = buffer

        self.buffer_control = BufferControl(
            buffer=self._buffer,
            lexer=PygmentsLexer(MarkdownLexer),
        )

        self.window = Frame(
            body=Window(
                content=self.buffer_control,
                right_margins=[ScrollbarMargin(display_arrows=True)],
                scroll_offsets=ScrollOffsets(top=2, bottom=2),
            ),
            title=self._title,
        )

    def __pt_container__(self):
        return self.window
