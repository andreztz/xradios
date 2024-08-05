import os
import logging
import logging.config
from logging.handlers import RotatingFileHandler

from appdirs import user_log_dir
from appdirs import user_data_dir
from appdirs import user_config_dir

from pathlib import Path

__version__ = "0.0.1.dev6"

app_name = "xradios"

xradios_config_dir = Path(user_config_dir(appname=app_name))
xradios_config_dir.mkdir(parents=True, exist_ok=True)
xradios_data_dir = Path(user_data_dir(appname=app_name))
xradios_data_dir.mkdir(parents=True, exist_ok=True)
xradios_log_dir = Path(user_log_dir(appname=app_name))
xradios_log_dir.mkdir(parents=True, exist_ok=True)

log_level = getattr(logging, os.environ.get("XRADIOS_LOG_LEVEL", "INFO"))

if log_level == logging.DEBUG:
    log_format = "%(levelname)s - %(name)s - %(filename)s -%(module)s - %(funcName)s - %(message)s"
else:
    log_format = "%(levelname)s - %(name)s - %(message)s"

log_file = "xradios.log"
# logging.config.dictConfig(config={"level": log_level, "handlers": [], "version": 1})
logging.basicConfig(level=log_level, format=log_format)

logging.getLogger().handlers = []
handler = RotatingFileHandler(
    filename=xradios_log_dir / log_file,
    maxBytes=5 * 1024 * 1024,
    backupCount=2
)
# handler.setLevel(log_level)
# handler.setFormatter(logging.Formatter(log_format))
logging.getLogger("xradiosd").addHandler(handler)
logging.getLogger("xradios").addHandler(handler)
