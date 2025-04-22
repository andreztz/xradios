import click

from xradios.__about__ import __version__
from xradios.ui import UI

app = UI()


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    invoke_without_command=True,
)
@click.version_option(version=__version__, prog_name="xradios")
def main():
    app.run()
