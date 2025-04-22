from streamscrobbler import streamscrobbler


def run(url, *args, **kwargs):
    data = streamscrobbler.get_server_info(url)
    metadata = data["metadata"]
    if not metadata:
        return
    return metadata.get("song").strip()
