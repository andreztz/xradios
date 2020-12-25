from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document

from xradios.logger import log
from xradios.tui.constants import LISTVIEW_BUFFER


class ListViewBuffer(Buffer):
    def __init__(self, *args, **kwargs):
        content = kwargs.get("content", "")
        super().__init__(
            document=Document(content, 0),
            multiline=True,
            read_only=True,
            name=LISTVIEW_BUFFER,
        )

    def line(self, index=None):

        if index and index.isnumeric():

            index = int(index) - 1

            line = self._get_line(index)
            return index, line

        # i (index) is -> (int) line number
        # text is -> (str) line content
        index = self.document.cursor_position_row
        text = self.document.current_line
        return index, text

    def _get_line(self, i):
        try:
            line = self.document.text.split("\n")[i]
        except IndexError:
            log.exception("ListViewBuffer._get_line(i)")
        else:
            return line

    def get_index(self, **kwargs):
        variables = kwargs.get("variables", None)
        index = variables.get("term") if variables else None

        if index and index.isnumeric():
            return self.line(index)[0]
        return self.line()[0]

    def update(self, content):
        self.reset(Document(content, 0))


buffer = ListViewBuffer()
