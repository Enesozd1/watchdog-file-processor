import logging
from typing import Any, Dict


def setup_logging(conf: Dict[str, Any]) -> None:
    logging.basicConfig(
        filename=conf["log_file"],
        level=getattr(logging, conf["log_level"]),
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
