import logging
from prompt_toolkit.contrib.regular_languages import compile
from xradios.tui.constants import DISPLAY_BUFFER
from xradios.tui.constants import LISTVIEW_BUFFER
from xradios.tui.constants import POPUP_BUFFER
from xradios.tui.constants import HELP_TEXT
from xradios.tui.client import proxy
from xradios.tui.utils import stations
from xradios.tui.utils import tags as _tags


log = logging.getLogger('xradios')


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


def grabe_from_buffer(buffer, stations, **kwargs):
    """
    Retrieves an object, via the line number of a given buffer.
    """
    index = int(buffer.get_index(**kwargs))
    station = stations[index]
    return index, station


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
    proxy.stop()
    event.app.exit()


@cmd("play")
def play(event, **kwargs):
    list_view_buffer = event.app.layout.get_buffer_by_name(LISTVIEW_BUFFER)
    index, station = grabe_from_buffer(
        list_view_buffer,
        stations,
        **kwargs
    )
    proxy.play(**station.serialize())
    display_buffer = event.app.layout.get_buffer_by_name(DISPLAY_BUFFER)
    metadata = proxy.now_playing()
    display_buffer.update(metadata)

    # from asyncio import get_event_loop
    # loop = get_event_loop()
    # loop.create_task(display_buffer.run())


@cmd("stop")
def stop(event, **kwargs):
    display_buffer = event.app.layout.get_buffer_by_name(DISPLAY_BUFFER)
    display_buffer.clear()
    proxy.stop()


@cmd("pause")
def pause(event, **kwargs):
    proxy.pause()


@cmd("search")
def search(event, **kwargs):
    query = {}
    list_buffer = event.app.layout.get_buffer_by_name(LISTVIEW_BUFFER)
    query["command"] = kwargs["variables"].get("subcommand")[2:]
    query["term"] = kwargs["variables"].get("term")
    stations.new(*proxy.search(**query))
    list_buffer.update(str(stations))

@cmd('tags')
def tags(event, **kwargs):
    list_buffer = event.app.layout.get_buffer_by_name(LISTVIEW_BUFFER)
    _tags.new(*proxy.tags())
    list_buffer.update(str(_tags))


@cmd("help")
def help(event, **kwargs):
    """Show help"""
    popup_buffer = event.app.layout.get_buffer_by_name(POPUP_BUFFER)
    popup_buffer.update(HELP_TEXT)
    event.app.layout.focus(popup_buffer)


@cmd('favorite')
def favorite(event, **kwargs):
    list_view_buffer = event.app.layout.get_buffer_by_name(
        LISTVIEW_BUFFER
    )
    subcommand = kwargs['variables'].get('subcommand')
    log.debug(f'{subcommand=}')
    match subcommand:
        case 'add':
            index, station = grabe_from_buffer(list_view_buffer, stations, **kwargs)
            station = station.serialize()
            # Removes `index` key before saving
            del station['index']
            proxy.add_favorite(**station)
        case 'remove':
            index, station = grabe_from_buffer(list_view_buffer, stations, **kwargs)
            station = station.serialize()
            proxy.remove_favorite(**station)
        case _:
            log.debug(f'{subcommand!r} not yet implemented')

    stations.new(*proxy.favorites())
    list_view_buffer.update(str(stations))


@cmd("favorites")
def favorites(event, **kwargs):
    """
    Go to favorites page
    """
    list_view_buffer = event.app.layout.get_buffer_by_name(LISTVIEW_BUFFER)
    stations.new(*proxy.favorites())
    list_view_buffer.update(str(stations))
