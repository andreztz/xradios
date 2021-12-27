import subprocess

from xradios.tui import TUI
from xradios.cli import parser
from xradios.tui.client import proxy

from pyradios import RadioBrowser
from tinydb import TinyDB

rb = RadioBrowser()
db = TinyDB('bookmarks.json')


def main():
    cli = parser.parse_args()
    query = {}

    server = "xradiosd"

    if cli.stations_by_tag:
        query['command'] = "bytag"
        query["term"] = cli.stations_by_tag
    else:
        query['command'] = "bytag"
        query["term"] = "trance"
    
    proc = subprocess.Popen(
        [server],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # response = proxy.remote_search(**query)

    response = db.all()

    tui = TUI()
    tui.initialize(response)
    tui.run()
    
    proc.terminate()
    proc.wait(timeout=2)
