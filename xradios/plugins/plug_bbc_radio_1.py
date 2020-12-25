import requests


URL = "https://rms.api.bbc.co.uk/v2/services/bbc_radio_one/segments/latest"


def run():
    resp = requests.get(URL)
    data = resp.json()
    try:
        artist = data['data'][0]['titles']['primary']
        song = data['data'][0]['titles']['secondary']
    except Exception:
        return None, None, None
    else:
        return "BBC Radio 1", artist, song


if __name__ == '__main__':
    print(run())
