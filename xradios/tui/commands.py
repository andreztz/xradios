from prompt_toolkit.contrib.regular_languages import compile

from xradios.tui.constants import DISPLAY_BUFFER
from xradios.tui.constants import LISTVIEW_BUFFER
from xradios.tui.constants import POPUP_BUFFER
from xradios.tui.constants import HELP_TEXT


from xradios.tui.messages import emitter
from xradios.tui.client import proxy
from xradios.tui.utils import stations


import logging


log = logging.getLogger(__name__)


COMMAND_GRAMMAR = compile(
    r"""(
        (?P<command>[^\s]+) \s+ (?P<subcommand>[^\s]+) \s+ (?P<term>[^\s].+) |
        (?P<command>[^\s]+) \s+ (?P<term>[^\s]+) |
        (?P<command>[^\s!]+)
    )"""
)


COMMAND_TO_HANDLER = {}


def get_commands():
    return COMMAND_TO_HANDLER.keys()


def get_command_help(command):
    return COMMAND_TO_HANDLER[command].__doc__


def has_command_handler(command):
    return command in COMMAND_TO_HANDLER


def call_command_handler(command, *args, **kwargs):
    COMMAND_TO_HANDLER[command](*args, **kwargs)


def listview_handler(event):
    call_command_handler("play", event)


def command_line_handler(event):
    try:
        variables = COMMAND_GRAMMAR.match(
            event.current_buffer.text
        ).variables()
    except Exception:
        return
    else:
        command = variables.get("command")
        if has_command_handler(command):
            call_command_handler(command, event, variables=variables)


def cmd(name):
    """
    Decorator to register commands in this namespace
    """

    def decorator(func):
        COMMAND_TO_HANDLER[name] = func

    return decorator


@cmd("exit")
def exit(event, **kwargs):
    """ exit Ctrl + Q"""
    emitter.emit("KILLALL")
    event.app.exit()


@cmd("play")
def play(event, **kwargs):
    list_buffer = event.app.layout.get_buffer_by_name(LISTVIEW_BUFFER)
    index = list_buffer.get_index(**kwargs)
    station = stations[int(index)]
    proxy.play(stationuuid=station.stationuuid)
    emitter.emit("INIT_RADIO_STATION_INFO", station=station.serialize())
    display_buffer = event.app.layout.get_buffer_by_name(DISPLAY_BUFFER)
    # emitter.emit("")
    metadata = emitter.emit("GET_RADIO_STATION_INFO")
    display_buffer.update(metadata)


@cmd("stop")
def stop(event, **kwargs):
    display_buffer = event.app.layout.get_buffer_by_name(DISPLAY_BUFFER)
    display_buffer.clear()
    proxy.stop()


@cmd("pause")
def pause(event, **kwargs):
    proxy.pause()


@cmd("list")
def list(event, **kwargs):
    list_buffer = event.app.layout.get_buffer_by_name(LISTVIEW_BUFFER)
    query = {}
    query["command"] = kwargs["variables"].get("subcommand")
    query["term"] = kwargs["variables"].get("term")
    response = proxy.remote_search(**query)
    stations.new(*response)
    list_buffer.update(str(stations))


@cmd("help")
def help(event, **kwargs):
    """Show help"""
    popup_buffer = event.app.layout.get_buffer_by_name(POPUP_BUFFER)
    popup_buffer.update(HELP_TEXT)
    event.app.layout.focus(popup_buffer)
