import subprocess
import time

from xradios.tui import TUI
from xradios.cli import parser
from xradios.tui.services import initialize as initialize_services
from xradios.tui.client import proxy

from pyradios import RadioBrowser


rb = RadioBrowser()


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
    # wait until the server is ready
    time.sleep(1)

    response = proxy.remote_search(**query)

    tui = TUI()
    tui.initialize(response)
    initialize_services()
    tui.run()
    
    proc.kill()
    proc.wait(timeout=1)
