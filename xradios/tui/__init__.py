from asyncio import get_event_loop

from prompt_toolkit.application import Application

from xradios.tui.buffers.listview import LISTVIEW_BUFFER
from xradios.tui.buffers.display import DISPLAY_BUFFER
from xradios.tui.keybindings import kbindings
from xradios.tui.layout import layout
from xradios.tui.utils import stations
from xradios.tui.client import proxy


class TUI:
    def __init__(self, *args, **kwargs):
        self.app = Application(
            layout=layout,
            key_bindings=kbindings(),
            full_screen=True,
            mouse_support=True,
            enable_page_navigation_bindings=True,
        )
        self.loop = get_event_loop()
        self.favorites = None

    def initialize(self):
        list_buffer = self.app.layout.get_buffer_by_name(LISTVIEW_BUFFER)
        response = self.get_favorites()
        stations.new(*response)
        list_buffer.update(str(stations))
        display_buffer = self.app.layout.get_buffer_by_name(DISPLAY_BUFFER)

        self.loop.create_task(display_buffer.run())

    def get_favorites(self):
        response = None
        while response is None:
            try:
                response = proxy.favorites()
            except:
                import time
                time.sleep(0.5)
            else:
                return response


    def run(self):
        self.app.run()
