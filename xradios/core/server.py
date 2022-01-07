import logging
import os
import sys
import signal

from pathlib import Path

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from appdirs import user_data_dir
from appdirs import user_log_dir
from appdirs import user_config_dir

from pyradios import RadioBrowser

from tinydb import Query
from tinydb import TinyDB

from xradios.core.metadata import metadata_manager
from xradios.core.player import player


app_name = 'xradios'
server_name = 'xradiosd'

xradios_config_dir = Path(user_config_dir(appname=app_name))
xradios_config_dir.mkdir(parents=True, exist_ok=True)

xradios_data_dir = Path(user_data_dir(appname=app_name))
xradios_data_dir.mkdir(parents=True, exist_ok=True)

xradios_log_dir = Path(user_log_dir(appname=app_name))
xradios_log_dir.mkdir(parents=True, exist_ok=True)

log_level = getattr(logging, os.environ.get('XRADIOS_LOG_LEVEL', 'INFO'))
log_format = '%(levelname)s - %(name)s - %(message)s'
log_file = 'xradios.log'

logging.basicConfig(
    filename=xradios_log_dir / log_file,
    level=log_level,
    format=log_format
    )

log = logging.getLogger('xradios')
effective_log_level = logging.getLevelName(log.getEffectiveLevel())
log.info(f'Log level {effective_log_level=}')


rb = RadioBrowser()
db = TinyDB(xradios_data_dir / 'favorites.json')


command_handlers = {}


def cmd(name):
    def decorator(func):
        command_handlers[name] = func
    return decorator


@cmd("play")
def play(**station):
    metadata_manager(station)
    player.play(station.get("stationuuid"))


@cmd("stop")
def stop():
    player.stop()


@cmd("pause")
def pause():
    player.pause()


@cmd("search")
def search(**kwargs):
    response = rb.search(**kwargs)
    return response


@cmd("tags")
def tags():
    response = rb.tags()
    return response


@cmd("now_playing")
def now_playing():
    metadata_manager.get()
    if player.playing:
        return metadata_manager.state()
    return


@cmd('favorites')
def favorites():

    stations = [dict(s) for s in db.all()]

    if stations:
        return stations
    else:
        return rb.stations_by_votes(limit=100)


@cmd('add_favorite')
def add_favorite(**station):
    # Check if the station has already been added to favorites
    if not db.search(Query().stationuuid == station['stationuuid']):
        db.insert(station)
    log.debug(f'Adding a new station to favorites {station=}')


@cmd('remove_favorite')
def remove_favorite(**station):
    db.remove(Query().stationuuid == station['stationuuid'])
    log.debug(f'Removing a station from favorites {station=}')


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/", "/RPC2")
    # def log_request(self, code="-", size="-"):
    #     from xradios.logger import log
    #     log.info(f'RPC status code {code}')
    #     BaseHTTPRequestHandler.log_message = lambda *args: print(*args)
    #     BaseHTTPRequestHandler.log_request(self, code, size)


class RPCServer:
    def __init__(self, address):
        self._serv = SimpleXMLRPCServer(
            address,
            allow_none=True,
            requestHandler=RequestHandler,
            use_builtin_types=True,
        )
        self._serv.rpc_paths = ("/", "/RPC2")  # default
        self._serv.register_introspection_functions()

        for key, value in command_handlers.items():
            setattr(self, key, value)
            self.register_function(getattr(self, key))

    def register_function(self, function, name=None):
        # https://stackoverflow.com/questions/119802/using-kwargs-with-simplexmlrpcserver-in-python
        def _function(args, kwargs):
            return function(*args, **kwargs)

        _function.__name__ = function.__name__
        self._serv.register_function(_function, name)

    def serve_forever(self):
        self._serv.serve_forever()

    def stop(self):
        self._serv.shutdown()


def sigterm_handler(signo, frame, server):
    server.stop()
    log.info('Shutdown server...')
    raise SystemExit(0)


def run(host="", port=10000):
    server = RPCServer((host, port))
    signal.signal(
        signal.SIGTERM,
        lambda signo, frame: sigterm_handler(signo, frame, server)
    )
    log.info(f"Serving XML-RPC port: {port}")
    server.serve_forever()


def main():
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
