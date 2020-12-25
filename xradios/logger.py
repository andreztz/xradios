import logging
import os


LEVEL = os.environ.get("CODERADIO_LOG_LEVEL", "INFO")
FORMAT = "%(levelname)s - %(name)s - %(message)s"

logging.basicConfig(
    filename="log.log", level=getattr(logging, LEVEL), format=FORMAT
)
log = logging.getLogger("coderadio")
