import logging
import signal
import sys

from jsonrpclib.SimpleJSONRPCServer import (
    SimpleJSONRPCRequestHandler,
    SimpleJSONRPCServer,
)
from pyradios import RadioBrowser
from tinydb import Query, TinyDB

from xradiosd import xradios_data_dir
from xradiosd.metadata import metadata_manager
from xradiosd.player import player

log = logging.getLogger("xradiosd")
effective_log_level = logging.getLevelName(log.getEffectiveLevel())
log.info(f"Log level {effective_log_level=}")


rb = RadioBrowser()
db = TinyDB(xradios_data_dir / "bookmarks.json")


command_handlers = {}


def cmd(name):
    """Decorator to register JSON-RPC methods."""
    def decorator(func):
        command_handlers[name] = func

    return decorator


@cmd("play")
def play(**station):
    """Starts playback of a radio station."""
    metadata_manager(station)
    player.play(station.get("stationuuid"))


@cmd("stop")
def stop():
    """Stop the current playback."""
    player.stop()


@cmd("pause")
def pause():
    """Pauses the current playback"""
    player.pause()


@cmd("search")
def search(**kwargs):
    """Searches for radio stations based on criteria."""
    response = rb.search(**kwargs)
    return response


@cmd("tags")
def tags():
    """Returns the available tags for stations."""
    response = rb.tags()
    return response


@cmd("now_playing")
def now_playing():
    """Returns information about the currently playing station."""
    if player.playing:
        metadata_manager.get()
        return metadata_manager.state()
    return


@cmd("bookmarks")
def bookmarks():
    """Returns the list of bookmarked stations or suggestions if empty."""
    stations = [dict(s) for s in db.all()]
    if stations:
        return stations
    else:
        return rb.stations_by_votes(limit=100)


@cmd("add_bookmark")
def add_bookmark(**station):
    """Adds a station to bookmarks."""
    # Check if the station has already been added to bookmarks
    if not db.search(Query().stationuuid == station["stationuuid"]):
        db.insert(station)
    log.debug(f"Adding a new station to bookmarks {station=}")


@cmd("remove_bookmark")
def remove_bookmark(**station):
    """Removes a station from bookmarks."""
    db.remove(Query().stationuuid == station["stationuuid"])
    log.debug(f"Removing a station from bookmarks {station=}")


class RequestHandler(SimpleJSONRPCRequestHandler):
    pass


class RPCServer:
    def __init__(self, address):
        self._serv = SimpleJSONRPCServer(
            address,
            requestHandler=RequestHandler,
        )
        self._serv.register_introspection_functions()

        for key, value in command_handlers.items():
            setattr(self, key, value)
            self.register_function(getattr(self, key))

    def register_function(self, function, name=None):
        def _function(*args, **kwargs):
            return function(*args, **kwargs)

        _function.__name__ = function.__name__
        self._serv.register_function(_function, name)

    def serve_forever(self):
        self._serv.serve_forever()

    def stop(self):
        self._serv.shutdown()


def sigterm_handler(signo, frame, server):
    server.stop()
    log.info("Shutdown server...")
    raise SystemExit(0)


def run(host="", port=10000):
    server = RPCServer((host, port))
    signal.signal(
        signal.SIGTERM,
        lambda signo, frame: sigterm_handler(signo, frame, server),
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
