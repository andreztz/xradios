import logging
import asyncio

from notify import notification

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document

from xradios.tui.constants import DISPLAY_BUFFER
from xradios.tui.client import proxy


log = logging.getLogger('xradios')


class DisplayBuffer(Buffer):
    def __init__(self, **kwargs):
        content = kwargs.get('content', '')
        super().__init__(
            document=Document(content, 0), read_only=True, name=DISPLAY_BUFFER
        )
        self._metadata = None

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        if value != self._metadata:
            self._metadata = value
            self.update(value)

    def clear(self):
        self.set_document(Document('', 0), bypass_readonly=True)

    async def run(self):
        while True:
            try:
                result = proxy.now_playing()
            except Exception:
                pass
            else:
                if all(result.values()):
                    self.metadata = result
            await asyncio.sleep(30)

    def update(self, metadata):
        name = metadata.get('name')
        homepage = metadata.get('homepage')
        song = metadata.get('song')

        if song:
            content = f"\n{name:<30} {homepage}\n\n{song}"
            try:
                notification(name, message=song, app_name="xradios", timeout=5000)
            except Exception:
                pass
                # TODO: log exception to text file
        else:
            content = f'\n{name:<30}\n\n{homepage}'
        
        self.set_document(Document(content, 0), bypass_readonly=True)


buffer = DisplayBuffer()
