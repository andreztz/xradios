from pathlib import Path

from cmd_parser.core import asdict, parse
from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.message import Message
from textual.reactive import reactive
from textual.screen import Screen
from textual.suggester import Suggester
from textual.validation import Function
from textual.widget import Widget
from textual.widgets import (
    DataTable,
    Footer,
    Input,
    MarkdownViewer,
    Placeholder,
    Static,
    TabbedContent,
    TabPane,
)
from textual.widgets.data_table import DuplicateKey
from textual.worker import Worker, get_current_worker

from xradios.client import proxy

COMMAND_LIST = [
    ":search",
    "name=",
    "name_exact=",
    "tag=",
    "tags=",
]


def _command_validator(command):
    if command:
        return True
    return False


class TopView(Static):
    DEFAULT_CSS = """
    TopView {
        dock: top;
        border: heavy green;
    }
    """

    text = reactive(default="")
    selected_row_index = reactive(default="0")
    metadata = reactive(default={})

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.core = self.set_interval(10.0, callback=self.request, pause=False)

    def render(self):
        return self.text

    @work(exclusive=True, thread=True)
    def request(self):
        worker = get_current_worker()
        if not worker.is_cancelled:
            try:
                response = proxy.now_playing()
                if response:
                    self.metadata = response
            except ConnectionRefusedError as exc:
                self.log(exc)
            except Exception as exc:
                self.log(exc)

    def watch_metadata(self, value):
        """
        Textual only calls `watch_` methods if the value of a reactive
        attribute changes. If the newly assigned value is the same as
        the previous value, the watch method is not called.
        """
        if value:
            name = value.get("name", "No name")
            song = value.get("song", "No song")
            home_page = value.get("homepage", "No web page")
            self.text = f"{name}    | Playing: {song} | Web Page: {home_page}"

    def init(self):
        self.request()

    def resume(self):
        self.core.resume()

    def stop(self):
        self.core.stop()


class ListViewUpdateMessage(Message, bubble=True):
    def __init__(self, content):
        self.content = content
        super().__init__()


class ListView(DataTable):
    BINDINGS = [
        Binding(
            key="p",
            action="play",
            description="Play",
            priority=False,
            key_display="p",
        ),
        Binding(
            key="s",
            action="stop",
            description="Stop",
            priority=False,
        ),
    ]
    selected_row_key = reactive(default="")
    buffer = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cursor_type = "row"
        self.styles.height = "1fr"
        self.selected_station = None

    def on_mount(self):
        response = {}

        try:
            response = proxy.bookmarks()
        except Exception as exc:
            self.log(exc)
            self.log("The server may be down")
        else:
            self.post_message(ListViewUpdateMessage(content=response))

    def fill(self, response):
        headers = ["name", "tags"]
        self.buffer.clear()
        self.clear()
        try:
            self.add_columns(*headers)
        except DuplicateKey:
            pass

        for station in response:
            row_content = [station.get(elem, f"No {elem}") for elem in headers]
            row_id = self.add_row(*row_content)
            self.buffer[row_id] = dict(
                filter(
                    lambda item: item[0]
                    in ["name", "tags", "homepage", "url", "stationuuid"],
                    station.items(),
                )
            )
        del response

    def on_data_table_row_highlighted(self, event):
        self.selected_row_key = event.row_key
        if self.buffer:
            self.selected_station: dict = self.buffer[self.selected_row_key]

    def action_stop(self):
        proxy.stop()

    def action_play(self):
        proxy.play(**self.selected_station)

    def on_key(self, event):
        station: dict = self.selected_station

        if event.key == "enter" and self.has_focus:
            try:
                proxy.play(**station)
            except Exception as exc:
                self.log(exc)
        elif event.key == "a" and self.has_focus:
            proxy.add_bookmark(**station)
            self.log("Add to bookmarks")
        elif event.key == "d" and self.has_focus:
            proxy.remove_bookmark(**station)
            self.log("Remove from bookmarks")
        elif event.key == "b" and self.has_focus:
            response = {}
            try:
                response = proxy.bookmarks()
            except Exception as exc:
                self.log(exc)
                self.log("The server may be down")
            else:
                self.post_message(ListViewUpdateMessage(content=response))


class CloseCommandLineMessage(Message, bubble=True):
    pass


class SubmitCommandLineMessage(Message, bubble=True):
    def __init__(self, command=None, **kwargs):
        self.command = command
        self.kwargs = kwargs
        super().__init__()


class CommandLineSuggester(Suggester):
    def __init__(
        self, *, use_cache: bool = True, case_sensitive: bool = False
    ) -> None:
        super().__init__(use_cache=use_cache, case_sensitive=case_sensitive)

    async def get_suggestion(self, value: str) -> str | None:
        hit = value[::-1].split()[0][::-1]

        for cmd in COMMAND_LIST:
            if cmd.startswith(hit):
                return value.replace(hit, cmd)

        return None


class CommandLine(Input):
    """
    Widget for run command
    """

    BINDINGS = [
        Binding(
            key="escape",
            action="close_command_mode",
            description="Close command line",
        ),
    ]
    DEFAULT_CSS = """
    CommandLine {
        background: $boost;
        color: $text;
        padding: 0 0;
        border: tall $background;
        width: 100%;
        height: 1;
        dock: bottom;
        border: none;
    }
    CommandLine.-disabled {
        opacity: 0.6;
    }
    CommandLine:focus {
       border: none;
    }
    CommandLine>.input--cursor {
        background: $surface;
        color: $text;
        text-style: reverse;
    }
    CommandLine>.input--placeholder {
        color: $text-disabled;
    }
    """

    def __init__(self, name=None, id=None, classes=None):
        super().__init__(
            name=name,
            id=id,
            classes=classes,
            validate_on=["submitted"],
            validators=[Function(_command_validator, "Input is not command")],
            select_on_focus=False,
            suggester=CommandLineSuggester(
                use_cache=False, case_sensitive=True
            ),
        )

    def action_close_command_mode(self):
        self.post_message(CloseCommandLineMessage())

    def on_focus(self):
        self.value = ":"

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        self.log(event)
        # self.log(event.worker.result)

    def on_input_submitted(self, message: Input.Submitted) -> None:
        options = asdict(parse(message.value))
        command = options.pop("command")
        del options["args"]
        kwargs = options.pop("kwargs")
        if not command and not kwargs:
            return
        self.post_message(SubmitCommandLineMessage(command, **kwargs))

    def watch_value(self, value):
        self.log(value)


class MainScreen(Screen):
    TITLE = "xradios"
    CSS_PATH = "style.css"
    BINDINGS = [
        Binding(
            key="colon",
            action="open_command_mode",
            description="Open Command Line",
            key_display=":",
        ),
        Binding("?", "app.push_screen('help')", "Help", key_display="?"),
        ("ctrl+up", "move_focus_up", "Up"),
        ("ctrl+down", "move_focus_down", "Down"),
    ]
    top_view: TopView
    list_view: ListView
    cmd_line_widget: CommandLine

    def compose(self) -> ComposeResult:
        yield TopView(name="TopView", id="top_view")
        with TabbedContent(initial="stations", classes="tab_content"):
            with TabPane("Stations", id="stations", classes="tab_pane"):
                yield ListView(name="list_view", classes="list_view")
            with TabPane("Bookmarks", id="bookmarks"):
                yield Placeholder(name="bookmarks")
        yield Footer()

    def on_mount(self):
        self.list_view = self.query_one(ListView)
        self.top_view = self.query_one(TopView)
        self.list_view.focus()
        self.top_view.init()

    def action_move_focus_up(self):
        """Focus List View widget and remove ComandLine widget"""
        self.list_view.focus()
        self.query(CommandLine).remove()

    def action_move_focus_down(self):
        """Mount and focus CommandLine widget"""
        self.cmd_line_widget = CommandLine(name="Command Line")
        self.mount(self.cmd_line_widget)
        self.cmd_line_widget.focus()

    def action_open_command_mode(self):
        """Mount and focus CommandLine widget"""
        self.cmd_line_widget = CommandLine(name="Command Line")
        self.mount(self.cmd_line_widget)
        self.cmd_line_widget.focus()

    def on_descendant_focus(self, widget: Widget):
        # WARNING: This is necessary so that when the focus is changed to
        # the 'list_view' widget using the mouse pointer, the 'command_line'
        # widget is correctly removed from the window.
        if self.list_view.has_focus:
            self.query(CommandLine).remove()

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Called when the worker state changes."""
        response = event.worker.result
        if response:
            self.post_message(ListViewUpdateMessage(content=response))

    @on(ListViewUpdateMessage)
    def update_list_view(self, event: ListViewUpdateMessage) -> None:
        list_view = self.query_one(ListView)
        list_view.fill(event.content)

    @on(CloseCommandLineMessage)
    def close_command_mode(self, event: CloseCommandLineMessage) -> None:
        list_view = self.query_one(ListView)
        list_view.focus()

    @on(SubmitCommandLineMessage)
    def submit_command_line(self, event: SubmitCommandLineMessage) -> None:
        response = self.http_handler(event.command, **event.kwargs)
        self.post_message(CloseCommandLineMessage())

    @work(exclusive=True, thread=True)
    def http_handler(self, command, **kwargs):
        client = getattr(proxy, command)
        worker = get_current_worker()
        client = getattr(proxy, command)
        if not worker.is_cancelled:
            response = client(**kwargs)
            self.log(response)
            return response


class Help(Screen):
    BINDINGS = [
        ("escape,space,q,question_mark", "app.pop_screen", "Close"),
    ]

    def compose(self) -> ComposeResult:
        yield MarkdownViewer(Path(__file__).with_suffix(".md").read_text())


class UI(App):
    SCREENS = {"help": Help}

    def on_mount(self):
        self.push_screen(MainScreen())
