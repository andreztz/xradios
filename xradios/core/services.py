import logging

from pyradios import RadioBrowser
from notify import notification

from xradios.messages import emitter
from xradios.core.player import Player
from xradios.core.metadata import Metadata


log = logging.getLogger(__name__)

metadata = Metadata()
player = Player()
rb = RadioBrowser()


def search(**kwargs):
    command = kwargs.get("command")
    term = kwargs.get("term")
    result = getattr(rb, "stations_by_{}".format(command[2:]))(term)
    return result


def killall():
    player.terminate()


def initialize():
    emitter.on("RADIO_PLAY", player.play)
    emitter.on("RADIO_STOP", player.stop)
    emitter.on("RADIO_PAUSE", player.pause)
    emitter.on("RADIO_SEARCH", search)
    emitter.on("METADATA_INIT", metadata)
    emitter.on("METADATA_GET", metadata.get)
    emitter.on("METADATA_STATE", metadata.state)
    emitter.on("NOTIFICATION", notification)
    emitter.on("KILLALL", killall)
