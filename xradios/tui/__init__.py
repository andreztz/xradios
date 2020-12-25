from prompt_toolkit.application import Application

from xradios.tui.buffers.listview import LISTVIEW_BUFFER
from xradios.tui.buffers.display import DISPLAY_BUFFER
from xradios.tui.keybindings import kbindings
from xradios.tui.layout import layout

from xradios.tui.utils import stations


class TUI:
    def __init__(self, *args, **kwargs):
        self.app = Application(
            layout=layout,
            key_bindings=kbindings(),
            full_screen=True,
            mouse_support=True,
            enable_page_navigation_bindings=True,
        )

    def initialize(self, *args, **kwargs):

        query = kwargs.get("query")
        search_term = kwargs.get("search_term")

        list_buffer = self.app.layout.get_buffer_by_name(LISTVIEW_BUFFER)
        stations.new(*query(search_term))
        list_buffer.update(str(stations))
        display_buffer = self.app.layout.get_buffer_by_name(DISPLAY_BUFFER)

        from asyncio import get_event_loop

        loop = get_event_loop()
        loop.create_task(display_buffer.run())

    def run(self):
        self.app.run()
