import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

import click
from appdirs import user_config_dir, user_data_dir, user_log_dir

from xradiosd.__about__ import __version__

app_name = "xradios"

xradios_config_dir = Path(user_config_dir(appname=app_name))
xradios_config_dir.mkdir(parents=True, exist_ok=True)
xradios_data_dir = Path(user_data_dir(appname=app_name))
xradios_data_dir.mkdir(parents=True, exist_ok=True)
xradios_log_dir = Path(user_log_dir(appname=app_name))
xradios_log_dir.mkdir(parents=True, exist_ok=True)

log_level = getattr(logging, os.environ.get("XRADIOS_LOG_LEVEL", "INFO"))

if log_level == logging.DEBUG:
    log_format = (
        "%(levelname)s - %(name)s - %(filename)s "
        "- %(module)s - %(funcName)s - %(message)s"
    )
else:
    log_format = "%(levelname)s - %(name)s - %(message)s"

log_file = "xradios.log"
logging.basicConfig(level=log_level, format=log_format)

logging.getLogger().handlers = []
handler = RotatingFileHandler(
    filename=xradios_log_dir / log_file,
    maxBytes=5 * 1024 * 1024,
    backupCount=2,
)
logging.getLogger("xradiosd").addHandler(handler)
logging.getLogger("xradios").addHandler(handler)


@click.command()
@click.version_option(version=__version__, prog_name="xradiosd")
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=10000, type=int)
def main(host, port):
    from xradiosd.server import run

    try:
        run(host, port)
    except KeyboardInterrupt:
        sys.exit(0)
