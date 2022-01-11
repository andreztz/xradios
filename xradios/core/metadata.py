import logging
import os
import re
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from functools import partial

from pluginbase import PluginBase


log = logging.getLogger('xradios')
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


@dataclass
class MetadataState:
    name: str = field(init=False, default="")
    song: str = field(init=False, default="")
    homepage: str = field(init=False, default="")

    def serialize(self):
        return asdict(self)


class MetadataManager:
    def __init__(self):
        self.station = None
        self.s = MetadataState()

    def get(self):
        """
        Try to find the id of the song that is playing.
        """
        song = None
        # BUG: clear song state
        self.s.song = ''

        name = plugin_name(self.station["name"])

        if name in plugin_source.list_plugins():
            # Try to get the id of song with user plugin.
            plugin = plugin_source.load_plugin(name)
            song = plugin.run()
        else:
            # Try to get the id of song with streamscrobler plugin.
            plugin = plugin_source.load_plugin("stream")
            song = plugin.run(self.station["url"])

        if song and isinstance(song, str):
            self.s.song = song
        else:
            log.debug(f'{song}= Must be string, not {type(song)=}')

    def state(self):
        return self.s.serialize()

    def __call__(self, station):
        if station:
            self.station = station
            self.s.homepage = station["homepage"]
            self.s.name = station["name"]


metadata_manager = MetadataManager()
