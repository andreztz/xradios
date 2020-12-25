from prompt_toolkit.layout import Float
from prompt_toolkit.layout import FloatContainer
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout import HSplit
from prompt_toolkit.layout import ConditionalContainer

from prompt_toolkit.filters import has_focus

from xradios.tui.widget.display import Display
from xradios.tui.widget.popup import PopupWindow
from xradios.tui.widget.listview import ListView
from xradios.tui.widget.prompt import Prompt
from xradios.tui.widget.topbar import TopBar

from xradios.tui.buffers.display import buffer as display_buffer
from xradios.tui.buffers.popup import buffer as popup_buffer
from xradios.tui.buffers.prompt import buffer as prompt_buffer
from xradios.tui.buffers.listview import buffer as listview_buffer


layout = Layout(
    FloatContainer(
        content=HSplit(
            [
                TopBar(message="Need help! Press `F1`."),
                Display(display_buffer),
                ListView(listview_buffer),
                Prompt(prompt_buffer),
            ]
        ),
        modal=True,
        floats=[
            # Help text as a float.
            Float(
                top=3,
                bottom=2,
                left=2,
                right=2,
                content=ConditionalContainer(
                    content=PopupWindow(
                        popup_buffer, title="Help"
                    ),
                    filter=has_focus(popup_buffer),
                ),
            )
        ],
    )
)


layout.focus(prompt_buffer)
