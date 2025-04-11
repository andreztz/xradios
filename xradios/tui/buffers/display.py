import logging
import asyncio
import os
import shutil
import subprocess


from prompt_toolkit.buffer import Buffer
from prompt_toolkit.document import Document

from xradios.tui.constants import DISPLAY_BUFFER
from xradios.tui.client import proxy


log = logging.getLogger("xradios")


notification_is_available = (
    os.environ.get("DISPLAY", None) is not None
    and shutil.which("notify-send") is not None
)


def _notification(name, message, app_name="xradios", timeout=5000):
    if not notification_is_available:
        return

    try:
        from notify import notification
        notification(name, message, app_name, timeout)
    except ImportError:
        pass  # fallback to notify-send command
    except Exception as exc:
        log.error(
            f"Failure to send notification via notify-send module: {exc}"
        )

    try:
        proc = subprocess.run(
            [
                "notify-send",
                name,
                message,
                "-a",
                app_name,
                "-t",
                str(timeout)
             ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,  # Segurança contra processos travados
            check=True
        )
        if proc.returncode != 0:
            log.debug(
                f"Failure in subprocess\nstdout: {proc.stdout.decode()}\n"
                f"stderr: {proc.stderr.decode()}"
            )
    except subprocess.CalledProcessError as exc:
        log.error(
            f"Failure to send notification via notify-send command: {exc}"
        )
    except FileNotFoundError:
        log.warning("notify-send: command not found")
    except Exception as exc:
        log.error(f"An unexpected error occurred: {exc}")

    return


class DisplayBuffer(Buffer):
    def __init__(self, **kwargs):
        content = kwargs.get("content", "")
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
        self.set_document(Document("", 0), bypass_readonly=True)

    async def run(self):
        while True:
            try:
                result = proxy.now_playing()
            except Exception:
                pass
            else:
                if result and all(result.values()):
                    self.metadata = result
            await asyncio.sleep(30)

    def update(self, metadata):
        name = metadata.get("name")
        homepage = metadata.get("homepage")
        song = metadata.get("song")

        if song:
            content = f"\n{name:<30} {homepage}\n\n{song}"
            try:
                _notification(
                    name, message=song, app_name="xradios", timeout=5000
                )
            except Exception:
                pass
                # TODO: log exception to text file

        else:
            content = f"\n{name:<30}\n\n{homepage}"

        self.set_document(Document(content, 0), bypass_readonly=True)


buffer = DisplayBuffer()
