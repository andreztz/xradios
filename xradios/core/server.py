# import logging
import os
import re
import sys
from dataclasses import dataclass
from dataclasses import field

from functools import partial

import signal
from signal import SIGTERM

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# from http.server import BaseHTTPRequestHandler
from pluginbase import PluginBase
from pyradios import RadioBrowser


from xradios.core.player import player
from xradios.logger import log


rb = RadioBrowser()


command_handlers = {}


def cmd(name):
    def decorator(func):
        command_handlers[name] = func

    return decorator


@cmd("play")
def play(*args, **kwargs):
    player.play(kwargs.get("stationuuid"))


@cmd("stop")
def stop(*args, **kwargs):
    player.stop()


@cmd("pause")
def pause():
    player.pause()


@cmd("local_search")
def local_search():
    log.info("procurando media localmente")


@cmd("remote_search")
def remote_search(**kwargs):
    command = kwargs.get("command")
    term = kwargs.get("term")
    result = getattr(rb, "stations_by_{}".format(command[2:]))(term)
    return result


from xradios.core.metadata import metadata_manager


@cmd("station_info")
def station_info(**kwargs):
    station = kwargs.get("station", None)
    metadata_manager(station)
    metadata_manager.get()
    return metadata_manager.state()


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
    raise SystemExit(1)


def run(host="", port=10000):
    server = RPCServer((host, port))
    signal.signal(
        signal.SIGTERM,
        lambda signo, frame: sigterm_handler(signo, frame, server)
    )

    log.info(f"Serving XML-RPC port: {port}")
    server.serve_forever()


def main():
    import sys

    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
