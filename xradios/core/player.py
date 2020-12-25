import logging

from mpv import MPV
from pyradios import RadioBrowser


rb = RadioBrowser()
log = logging.getLogger(__name__)


class Player:
    player = MPV(
        video=False,
        ytdl=False,
        input_default_bindings=True,
        input_vo_keyboard=True,
    )
    player.fullscreen = False
    player.loop_playlist = "inf"
    player["vo"] = "gpu"
    player.set_loglevel = "no"

    def play(self, station):
        url = self._click_counter(station.stationuuid)
        self.player.play(url)
        # self.player.wait_for_playback() # Block

    def stop(self):
        self.player.play("")

    def pause(self):
        if self.player.pause:
            self.player.pause = False
        else:
            self.player.pause = True

    def terminate(self):
        self.player.terminate()

    def _click_counter(self, stationuuid):
        try:
            station = rb.click_counter(stationuuid)
        except Exception:
            log.exception("Playable Station Error:")
        else:
            return station["url"]
