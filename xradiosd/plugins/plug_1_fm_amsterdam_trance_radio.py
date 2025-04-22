import httpx

url = "https://www.1.fm/stplaylist/atr"


def run(*args, **kwargs):
    try:
        resp = httpx.get(url)
        obj = resp.json()
        artist = obj["nowplaying"][0]["artist"]
        title = obj["nowplaying"][0]["title"]
        return "{} - {}".format(artist, title)
    except Exception:
        return


if __name__ == '__main__':
    print(run())
