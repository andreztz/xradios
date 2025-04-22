import logging
from abc import ABC, abstractmethod

from mpv import MPV
from pyradios import RadioBrowser

rb = RadioBrowser()
log = logging.getLogger('xradiosd')


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


def log_handler(level, prefix, message):
    func = getattr(log, level.lower(), log.info)  # getattr default -> log.info
    func(f"{prefix}: {message}")


class MPVPlayer(PlayerBase):
    extra_mpv_opts = {
        "cache": True,
        "cache_secs": 10,
        "loop-playlist": "force"
    }

    player = MPV(
        log_handler=log_handler,
        loglevel=logging.getLevelName(log.root.level).lower(),
        **extra_mpv_opts,
    )
    log.debug(f"mpv --cache ---> {player['cache']}")
    log.debug(f"mpv --cache-secs ---> {player.cache_secs}")

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


player = MPVPlayer()
