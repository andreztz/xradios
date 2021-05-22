import requests


url = "https://www.1.fm/stplaylist/atr"


def run(*args, **kwargs):
    try:
        resp = requests.get(url)
        obj = resp.json()
        artist = obj["nowplaying"][0]["artist"]
        title = obj["nowplaying"][0]["title"]
        return "{} - {}".format(artist, title)
    except Exception:
        return
