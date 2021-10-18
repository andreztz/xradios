import asyncio

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document


from xradios.tui.messages import emitter
from xradios.tui.constants import DISPLAY_BUFFER

import logging

log = logging.getLogger('xradios')


class DisplayBuffer(Buffer):
    def __init__(self, *args, **kwargs):
        content = kwargs.get("content", "")
        super().__init__(
            document=Document(content, 0), read_only=True, name=DISPLAY_BUFFER
        )

    def clear(self):
        self.set_document(Document("", 0), bypass_readonly=True)

    def format_display(self, m):
        m = type('M', (object, ), m)
        if m.play_now:
            return (
                f"\n{m.index:>4} | {m.name:<30} {m.homepage}\n\n   {m.play_now}"
            )
        return f"\n{m.index} | {m.name}\n\nWebsite: {m.homepage}\n"

    async def run(self):
        while True:
            try:
                metadata = emitter.emit("GET_RADIO_STATION_INFO")
            except:
                pass
            else:
                # if metadata and metadata.play_now and metadata.name:
                    # emitter.emit(
                    #   "NOTIFICATION", metadata.play_now, metadata.name
                    # )
                log.info(metadata)
                self.update(metadata)
            await asyncio.sleep(120)

    def update(self, metadata):
        content = self.format_display(metadata)
        self.set_document(Document(content, 0), bypass_readonly=True)


buffer = DisplayBuffer()
