from prompt_toolkit.widgets import Box
from prompt_toolkit.widgets import Label


class TopBar:
    def __init__(self, message):
        self.window = Box(
            Label(text=message),
            padding_left=2,
            height=1
        )

    def __pt_container__(self):
        return self.window
