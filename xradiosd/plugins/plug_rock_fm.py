import time

import httpx

URL = f"https://meta.fmgid.com/stations/rock/current.json?t={int(time.time())}"


def run(*args, **kwargs):
    resp = httpx.get(URL)
    data = resp.json()
    try:
        artist = data["artist"]
        title = data["title"]
    except Exception:
        return
    else:
        return "{} - {}".format(artist, title)


if __name__ == "__main__":
    print(run())
