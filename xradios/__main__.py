from xradios.tui import TUI
from xradios.cli import parser
from xradios.tui.services import initialize as initialize_services
from xradios.tui.client import proxy
from xradios.logger import log

from pyradios import RadioBrowser


rb = RadioBrowser()


def main():

    cli = parser.parse_args()
    query = {}

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


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log.exception()
