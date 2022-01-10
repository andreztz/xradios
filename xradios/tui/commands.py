import logging
import re
from itertools import chain
from itertools import tee
from distutils.util import strtobool

from prompt_toolkit.contrib.regular_languages import compile
from xradios.tui.constants import DISPLAY_BUFFER
from xradios.tui.constants import LISTVIEW_BUFFER
from xradios.tui.constants import POPUP_BUFFER
from xradios.tui.constants import HELP_TEXT
from xradios.tui.client import proxy
from xradios.tui.utils import stations
from xradios.tui.utils import tags as _tags


log = logging.getLogger('xradios')

# (?P<command>[^\s]+)\s+(?P<term>[^\s]+)|

COMMAND_GRAMMAR = compile(
    r"""(
        (?P<command>[^\s]+)\s+(?P<subcommand>.+)|
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
    index = int(buffer.get_index(**kwargs))
    station = stations[index]
    return index, station


def auto_cast(value):
    """
    Helper to convert types.
    """
    value = str(value).strip()

    if value.isnumeric():
        value = int(value)
    elif value.lower() in ['true', 'false']:
        value = bool(strtobool(value))
    return value


def getopts(string):
    opts = {}
    pattern = '''[a-zA-Z_]+='''

    # checks the indices of each paramters and argument in the string.
    isymbols = [(m.start(0), m.end(0)) for m in re.finditer(pattern, string)]
    flatten = list(chain.from_iterable(isymbols))

    def pairwise(iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)

    def parse_opts(iterable):
        for elem in iterable:
            start, end = elem
            yield string[start:end]
        yield string[elem[1]:]  # return the last argument of search command

    last = None
    search_params = [
        'name',
        'nameExact',
        'country',
        'countryExact',
        'countrycode',
        'state',
        'stateExact',
        'tagList',
        'codec',
        'bitrateMin',
        'bitrateMax',
        'has_geo_info',
        'has_extended_info',
        'is_https',
        'order',
        'reverse',
        'offset',
        'limit',
        'hidebroken',
        'tag'
        ]

    for i in parse_opts(pairwise(flatten)):
        if '=' in i:
            # process params
            key = i[:-1]  # clean paramter `tag=` -> `tag`
            if key not in search_params:
                return {}
            opts.setdefault(key)
            last = key
        else:
            # process args
            opts.update({last: auto_cast(i)})
    return opts


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
    options = kwargs['variables'].get('subcommand')
    query = getopts(options)

    if query:
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
    match subcommand:
        case 'add':
            index, station = grabe_from_buffer(
                list_view_buffer, stations, **kwargs
            )
            station = station.serialize()
            # Removes `index` key before saving
            del station['index']
            proxy.add_favorite(**station)
        case 'remove':
            index, station = grabe_from_buffer(
                list_view_buffer, stations, **kwargs
            )
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
