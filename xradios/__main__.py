import sys
import asyncio
import subprocess

from xradios.tui import TUI
from xradios.cli import parser


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

    tui = TUI()
    asyncio.get_event_loop().run_until_complete(tui.run())
    proc.terminate()
    sys.exit(proc.wait(timeout=5))
