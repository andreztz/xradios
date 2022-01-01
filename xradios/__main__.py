import time
import logging
import subprocess

from xradios.tui import TUI
from xradios.cli import parser
from xradios.tui.client import proxy


def main():
    cli = parser.parse_args()
    query = {}
    if cli.stations_by_tag:
        query['command'] = "bytag"
        query["term"] = cli.stations_by_tag
    else:
        query['command'] = "bytag"
        query["term"] = "trance"
    proc = subprocess.Popen(
        ['xradiosd'],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2)
    response = proxy.bookmarks()
    # response = proxy.search(**query)
    tui = TUI()
    tui.initialize(response)
    tui.run()
    proc.terminate()
    proc.wait(timeout=2)
