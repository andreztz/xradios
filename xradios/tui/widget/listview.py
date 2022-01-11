from prompt_toolkit.keys import Keys
from prompt_toolkit.layout import BufferControl
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.margins import NumberedMargin
from prompt_toolkit.layout.margins import ScrollbarMargin
from prompt_toolkit.widgets import Box
from prompt_toolkit.widgets import Frame
from prompt_toolkit.key_binding import KeyBindings

from xradios.tui.commands import call_command_handler


class ListView:
    def __init__(self, buffer):

        self.buffer_control = BufferControl(
            buffer=buffer,
            focusable=True,
            key_bindings=self._get_key_bindings(),
            focus_on_click=True,
        )

        self.window = Window(
            content=self.buffer_control,
            right_margins=[ScrollbarMargin(display_arrows=True)],
            left_margins=[NumberedMargin()],
        )
        self.window = Frame(self.window)
        self.container = self.window

    def _get_key_bindings(self):
        "Key bindings for the List."
        kb = KeyBindings()

        @kb.add("p")
        @kb.add("enter")
        def _(event):
            call_command_handler('play', event)

        @kb.add("s")
        def _(event):
            call_command_handler('stop', event)

        @kb.add(Keys.ControlD)
        def _(event):
            index = int(event.current_buffer.document.cursor_position_row) + 1
            call_command_handler(
                'favorite-add', event, variables={'subcommand': index}
            )

        @kb.add(Keys.ControlA)
        def _(event):
            index = int(event.current_buffer.document.cursor_position_row) + 1
            call_command_handler(
                'favorite-rm', event, variables={'subcommand': index}
            )

        return kb

    def __pt_container__(self):
        return self.container
