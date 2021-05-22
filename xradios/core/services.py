import logging

from notify import notification
from pyradios import RadioBrowser
from xradios.core.metadata import MetadataManager
from xradios.core.player import Player
from xradios.messages import emitter


log = logging.getLogger(__name__)

metadata = MetadataManager()
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
