import requests


URL = "https://rms.api.bbc.co.uk/v2/services/bbc_radio_one/segments/latest"


def run(*args, **kwargs):
    resp = requests.get(URL)
    data = resp.json()
    try:
        artist = data["data"][0]["titles"]["primary"]
        title = data["data"][0]["titles"]["secondary"]
    except Exception:
        return
    else:
        return "{} - {}".format(artist, title)


if __name__ == "__main__":
    print(run())
