"""
Modul logging untuk Hunterbot.

Logging dalam bahasa Indonesia untuk kemudahan debugging.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from hunterbot.config import Config
from hunterbot import config as config_module

# Level names dalam Bahasa Indonesia
LEVEL_NAMES = {
    logging.DEBUG: "DEBUG",
    logging.INFO: "INFO",
    logging.WARNING: "PERINGATAN",
    logging.ERROR: "ERROR",
    logging.CRITICAL: "KRITIS"
}


class IndonesianFormatter(logging.Formatter):
    """Formatter custom untuk log dalam Bahasa Indonesia."""

    def __init__(self):
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        super().__init__(fmt, datefmt=Config.LOG_DATE_FORMAT)

    def format(self, record):
        # Terjemahkan level name ke Bahasa Indonesia
        record.levelname = LEVEL_NAMES.get(record.levelno, record.levelname)
        return super().format(record)


def setup_logging(log_level: str = None) -> None:
    """
    Setup logging untuk seluruh aplikasi.

    Args:
        log_level: Level logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                   Default dari Config.LOG_LEVEL.
    """
    if log_level is None:
        log_level = Config.LOG_LEVEL

    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level))

    # Hapus handler yang sudah ada
    root_logger.handlers.clear()

    # Buat file handler
    log_file = config_module.LOGS_DIR / f"hunterbot_{datetime.now():%Y%m%d}.log"
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(IndonesianFormatter())

    # Buat console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(IndonesianFormatter())

    # Tambah handlers
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    logging.info("Logging sistem diinisialisasi")


def get_logger(name: str) -> logging.Logger:
    """
    Ambil logger instance untuk modul tertentu.

    Args:
        name: Nama modul (biasanya __name__).

    Returns:
        Logger instance untuk modul tersebut.
    """
    return logging.getLogger(name)
