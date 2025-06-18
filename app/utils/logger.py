import logging
from datetime import datetime
from pathlib import Path

from app.utils.env_constants import LOGS_DIR


def get_logger(session_id: str) -> logging.Logger:
    logger_name = f"logger_{session_id}"
    date = datetime.now().strftime("%Y%m%d")

    log_formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    log_file = Path(LOGS_DIR) / date / f"log_{session_id}.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
    file_handler.setFormatter(log_formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.propagate = False

    return logger