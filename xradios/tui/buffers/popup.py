from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document

from xradios.tui.constants import POPUP_BUFFER


class PopupBuffer(Buffer):
    def __init__(self, *args, **kwargs):
        content = kwargs.get("content", "")
        super().__init__(
            document=Document(content, 0),
            read_only=True,
            name=POPUP_BUFFER
        )

    def update(self, content):
        self.reset(Document(content, 0))


buffer = PopupBuffer()
