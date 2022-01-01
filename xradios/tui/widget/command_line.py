from prompt_toolkit.layout import BufferControl
from prompt_toolkit.layout.processors import BeforeInput
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import ConditionalContainer
from prompt_toolkit.filters import has_focus

from xradios.tui.commands import command_line_handler


class CommandLine(ConditionalContainer):

    def __init__(self, buffer, filter=False):
        self.buffer = buffer
        self._buffer_control = BufferControl(
            buffer=self.buffer,
            input_processors=[BeforeInput(":")],
            key_bindings=self.kbindings(),
        )

        super().__init__(
            Window(self._buffer_control, height=1), filter=has_focus(buffer)
        )

    def kbindings(self):

        kb = KeyBindings()

        @kb.add("enter")
        def _(event):
            command_line_handler(event)
            self.buffer.text = ""

        return kb

