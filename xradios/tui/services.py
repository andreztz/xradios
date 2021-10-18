import logging

from notify import notification
from pyradios import RadioBrowser
from xradios.tui.messages import emitter
from xradios.tui.client import proxy


log = logging.getLogger(__name__)
rb = RadioBrowser()


def search(**kwargs):
    command = kwargs.get("command")
    term = kwargs.get("term")
    result = getattr(rb, "stations_by_{}".format(command[2:]))(term)
    return result


def initialize():
    emitter.on("INIT_RADIO_STATION_INFO", proxy.station_info)
    emitter.on("GET_RADIO_STATION_INFO", proxy.station_info)
    # emitter.on("METADATA_STATE", metadata.state)
    # emitter.on("NOTIFICATION", notification)
    # emitter.on("KILLALL", killall)
