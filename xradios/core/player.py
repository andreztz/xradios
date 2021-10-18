import logging

from mpv import MPV
from pyradios import RadioBrowser


rb = RadioBrowser()
log = logging.getLogger(__name__)


class Player:
    player = MPV()
    # player.loop_playlist = "inf"
    player.set_loglevel = "no"

    def play(self, stationuuid):
        url = self._click_counter(stationuuid)
        self.player.play(url)

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
            log.exception("click counter error:")
        else:
            return station["url"]


player = Player()
