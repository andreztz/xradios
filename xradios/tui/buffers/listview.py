import logging

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document

from xradios.tui.constants import LISTVIEW_BUFFER


log = logging.getLogger('xradios')


class ListViewBuffer(Buffer):
    def __init__(self, *args, **kwargs):
        content = kwargs.get("content", "")
        super().__init__(
            document=Document(content, 0),
            multiline=False,
            read_only=True,
            name=LISTVIEW_BUFFER,
        )

    def update(self, content):
        self.reset(Document(content, 0))


buffer = ListViewBuffer()
