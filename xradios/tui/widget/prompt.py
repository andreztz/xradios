from prompt_toolkit.layout import BufferControl
from prompt_toolkit.layout.processors import BeforeInput
from prompt_toolkit.layout import Float
from prompt_toolkit.layout import FloatContainer
from prompt_toolkit.widgets import Frame
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout import CompletionsMenu
from prompt_toolkit.key_binding import KeyBindings


from xradios.tui.commands import prompt_handler


class Prompt:
    def __init__(self, buffer, **kwargs):
        self.buffer = buffer
        self.before_input_text = kwargs.get("before_input_text", "➜ ")
        self.title = kwargs.get("title", "COMMAND SHELL")
        self._buffer = buffer
        self._buffer_control = BufferControl(
            buffer=self.buffer,
            input_processors=[
                BeforeInput(text=self.before_input_text)
            ],
            focus_on_click=True,
        )
        self.window = Frame(
            title=self.title,
            key_bindings=self.kbindings(),
            body=FloatContainer(
                content=Window(self._buffer_control),
                key_bindings=None,
                floats=[
                    Float(
                        xcursor=True,
                        ycursor=True,
                        content=CompletionsMenu(
                            max_height=5,
                            scroll_offset=1
                        ),
                    )
                ],
            ),
            height=3,
        )

    def kbindings(self):

        kb = KeyBindings()

        @kb.add("enter")
        def _(event):
            prompt_handler(event)
            self.buffer.text = ""
        return kb

    def __pt_container__(self):
        return self.window
