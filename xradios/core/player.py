import logging

from abc import ABC
from abc import abstractmethod
from mpv import MPV
from pyradios import RadioBrowser


rb = RadioBrowser()
log = logging.getLogger('xradios')


class PlayerBase(ABC):

    state = False

    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def _click_counter(self, stationuuid):
        try:
            station = rb.click_counter(stationuuid)
        except Exception:
            log.exception("click counter error:")
        else:
            return station["url"]

    @property
    def playing(self):
        return self.state


class MPVPlayer(PlayerBase):

    player = MPV()
    # player.loop_playlist = "inf"
    player.set_loglevel = "no"

    def play(self, stationuuid):
        url = self._click_counter(stationuuid)
        self.player.play(url)
        self.state = True

    def stop(self):
        self.player.play("")
        self.state = False

    def pause(self):
        if self.player.pause:
            self.player.pause = False
        else:
            self.player.pause = True

    def terminate(self):
        self.player.terminate()


class VLCPlayer(PlayerBase):
    import vlc
    instance = vlc.Instance("--input-repeat=-1")  # --verbose 0
    player = instance.media_player_new()

    def play(self, stationuuid):
        url = self._click_counter(stationuuid)
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()
        self.state = True

    def stop(self):
        self.player.stop()
        self.state = False


# player = MPVPlayer()
player = VLCPlayer()
