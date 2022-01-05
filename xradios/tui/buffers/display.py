import logging
import asyncio

from notify import notification

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document

from xradios.tui.constants import DISPLAY_BUFFER
from xradios.tui.client import proxy


log = logging.getLogger('xradios')


class DisplayBuffer(Buffer):
    def __init__(self, *args, **kwargs):
        content = kwargs.get("content", "")
        super().__init__(
            document=Document(content, 0),
            read_only=True,
            name=DISPLAY_BUFFER
        )

    def clear(self):
        self.set_document(Document("", 0), bypass_readonly=True)

    async def run(self):
        while True:
            try:
                metadata = proxy.now_playing()
            except:
                pass
            else:
                if metadata and all(metadata.values()):
                    notification(
                        metadata.get('name'),
                        message=metadata.get('song'),
                        app_name='xradios'
                    )

                    self.update(metadata)
            await asyncio.sleep(120)

    def update(self, metadata):
        log.info(metadata)
        if metadata.get('song'):
            content = '\n{name:<30} {homepage}\n\n{song}'.format(**metadata)
        else:
            content = "\n{name:<30}\n\n{homepage}".format(**metadata)

        self.set_document(Document(content, 0), bypass_readonly=True)


buffer = DisplayBuffer()
