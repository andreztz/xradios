import logging
import os
import re
from functools import partial
from pathlib import Path

from pluginbase import PluginBase
from streamscrobbler import streamscrobbler


log = logging.getLogger(__name__)

here = os.path.abspath(os.path.dirname(__file__))
get_path = partial(os.path.join, here)
plugin_base = PluginBase(package="xradios.plugins")

plugin_source = plugin_base.make_plugin_source(
    searchpath=[get_path("../plugins")]
)


def normalize_plugin_name(name):
    name = re.sub(r"(\s|\-|\.|,|\"|\'|\`)+", "_", name)
    return name.lower()


def plugin_name(name):
    return "plug_{}".format(normalize_plugin_name(name))


class MetadataState:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.play_now = ""
        self.homepage = ""

    def __repr__(self):
        return "MetadataState([{}, {}, {}])".format(
            self.name, self.play_now, self.homepage
        )


class MetadataManager:
    def __init__(self):
        self.station = None
        self.s = MetadataState()

    def get(self):
        """
        Try to find the id of the song that is playing.
        """
        song = None
        name = plugin_name(self.station.name)

        if name in plugin_source.list_plugins():
            # Try to get the id of song with user plugin.
            plugin = plugin_source.load_plugin(name)
            song = plugin.run()
        else:
            # Try to get the id of song with streamscrobler plugin.
            plugin = plugin_source.load_plugin("stream")
            song = plugin.run(station.url)

        if song:
            self.s.play_now = song

    def state(self):
        return self.s

    def __call__(self, station):
        self.station = station
        self.s.id = self.station.id
        self.s.homepage = self.station.homepage
        self.s.name = self.station.name
