from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document
from prompt_toolkit.completion import WordCompleter

from prompt_toolkit.layout import BufferControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.widgets import Frame
from prompt_toolkit.widgets import Box


class Display:
    def __init__(self, buffer):
        self.buffer_control = BufferControl(
            buffer=buffer,
            focusable=False,
            focus_on_click=False
        )
        self.window = Window(content=self.buffer_control)
        self.window = Frame(
            body=Box(self.window, padding_left=2, padding_right=0),
            height=7
        )

    def __pt_container__(self):
        return self.window
