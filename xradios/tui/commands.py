import logging

from cmd_parser.core import parse, asdict

from xradios.tui.constants import DISPLAY_BUFFER
from xradios.tui.constants import LISTVIEW_BUFFER
from xradios.tui.constants import POPUP_BUFFER
from xradios.tui.constants import HELP_TEXT
from xradios.tui.client import proxy
from xradios.tui.utils import stations
from xradios.tui.utils import tags as _tags


log = logging.getLogger('xradios')

COMMAND_TO_HANDLER = {}


def get_commands():
    return COMMAND_TO_HANDLER.keys()


def get_command_help(command):
    return COMMAND_TO_HANDLER[command].__doc__


def has_command_handler(command):
    return command in COMMAND_TO_HANDLER


def call_command_handler(command, *args, **kwargs):
    COMMAND_TO_HANDLER[command](*args, **kwargs)


def command_line_handler(event):
    command_string = ':' + event.current_buffer.text

    options = asdict(parse(string=command_string))

    command = options.get('command', '')
    if not has_command_handler(command):
        return

    del options['command']
    args = options['args']
    kwargs = options['kwargs']
    call_command_handler(command, event, *args, **kwargs)


def cmd(name):
    """
    Decorator to register commands in this namespace
    """
    def decorator(func):
        COMMAND_TO_HANDLER[name] = func

    return decorator


@cmd('exit')
def exit(event, **kwargs):
    """exit Ctrl + Q"""
    proxy.stop()
    event.app.exit()


@cmd('play')
def play(event, *args, **kwargs):
    if args:
        index = int(args[0]) - 1
    else:
        index = int(event.current_buffer.document.cursor_position_row)

    station = stations[index]
    proxy.play(**station.serialize())
    display_buffer = event.app.layout.get_buffer_by_name(DISPLAY_BUFFER)
    metadata = proxy.now_playing()
    display_buffer.update(metadata)


@cmd('stop')
def stop(event, **kwargs):
    display_buffer = event.app.layout.get_buffer_by_name(DISPLAY_BUFFER)
    display_buffer.clear()
    proxy.stop()


@cmd('pause')
def pause(event, **kwargs):
    proxy.pause()


@cmd('search')
def search(event, **kwargs):

    list_buffer = event.app.layout.get_buffer_by_name(LISTVIEW_BUFFER)
    stations.new(*proxy.search(**kwargs))
    list_buffer.update(str(stations))


@cmd('tags')
def tags(event, **kwargs):
    list_buffer = event.app.layout.get_buffer_by_name(LISTVIEW_BUFFER)
    _tags.new(*proxy.tags())
    list_buffer.update(str(_tags))


@cmd('help')
def help(event, **kwargs):
    """Show help"""
    popup_buffer = event.app.layout.get_buffer_by_name(POPUP_BUFFER)
    popup_buffer.update(HELP_TEXT)
    event.app.layout.focus(popup_buffer)


@cmd('bookmarks')
def bookmark(event, *args, **kwargs):
    list_view_buffer = event.app.layout.get_buffer_by_name(LISTVIEW_BUFFER)

    match kwargs:
        case {'add': _}:
            index = int(kwargs['add']) - 1
            station = stations[index]
            station = station.serialize()
            proxy.add_favorite(**station)
            stations.new(*proxy.favorites())
            list_view_buffer.update(str(stations))
        case {'rm': _}:
            index = int(kwargs['rm']) - 1
            station = stations[index]
            station = station.serialize()
            proxy.remove_favorite(**station)
            stations.new(*proxy.favorites())
            list_view_buffer.update(str(stations))
        case _:
            stations.new(*proxy.favorites())
            list_view_buffer.update(str(stations))
