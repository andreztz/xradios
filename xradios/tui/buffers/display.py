import asyncio

from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document

from xradios.logger import log
from xradios.messages import emitter
from xradios.tui.constants import DISPLAY_BUFFER


class DisplayBuffer(Buffer):
    def __init__(self, *args, **kwargs):
        content = kwargs.get("content", "")
        super().__init__(
            document=Document(content, 0), read_only=True, name=DISPLAY_BUFFER
        )

    def clear(self):
        self.set_document(Document("", 0), bypass_readonly=True)

    def format_display(self, m):

        if m.play_now:
            return (
                f"\n{m.id:>4} | {m.name:<30} {m.homepage}\n\n   {m.play_now}"
            )

        return f"\n{m.id} | {m.name}\n\nWebsite: {m.homepage}\n"

    async def run(self):
        while True:
            try:

                emitter.emit("METADATA_GET")
            except:
                pass

            metadata = emitter.emit("METADATA_STATE")

            if metadata and metadata.play_now and metadata.name:
                emitter.emit("NOTIFICATION", metadata.play_now, metadata.name)
            log.info(metadata)
            self.update(metadata)

            await asyncio.sleep(120)

    def update(self, metadata):
        content = self.format_display(metadata)
        self.set_document(Document(content, 0), bypass_readonly=True)


buffer = DisplayBuffer()
