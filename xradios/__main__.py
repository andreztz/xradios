import os 
import subprocess
import signal
import time

import psutil

from xradios.tui import TUI
from xradios.cli import parser
from xradios.tui.services import initialize as initialize_services
from xradios.tui.client import proxy
from xradios.logger import log

from pyradios import RadioBrowser


rb = RadioBrowser()


def process_is_running(cmd):
    return any(
        process for process in psutil.process_iter()
        if cmd.lower() in process.name().lower()
        )

def kill_server(pid):
    os.kill(pid, signal.SIGTERM)


def main():
    cli = parser.parse_args()
    query = {}

    server = "xradiosd"

    subprocess.Popen(
        [server],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    time.sleep(5)

    if cli.stations_by_tag:
        query['command'] = "bytag"
        query["term"] = cli.stations_by_tag
    else:
        query['command'] = "bytag"
        query["term"] = "trance"

    response = proxy.remote_search(**query)

    tui = TUI()
    tui.initialize(response)
    initialize_services()
    tui.run()

    if process_is_running(server):
        pid = None
        for process in psutil.process_iter():
            if server in process.name():
                pid = int(process.pid)
        if pid:
            kill_server(pid)
