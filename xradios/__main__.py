from xradios.tui import TUI
from xradios.cli import parser
from xradios.core.services import initialize as initialize_services

from pyradios import RadioBrowser

rb = RadioBrowser()


def main():
    cli = parser.parse_args()

    if cli.stations_by_tag:
        query = getattr(rb, "stations_by_tag")
        search_term = cli.stations_by_tag
    else:
        query = getattr(rb, "stations_by_tag")
        search_term = "bbc"

    tui = TUI()
    tui.initialize(query=query, search_term=search_term)
    initialize_services()
    tui.run()


if __name__ == "__main__":
    main()
