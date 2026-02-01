"""
Entry point utama aplikasi Hunterbot.

File ini adalah starting point untuk menjalankan aplikasi.
"""

import sys
import logging

from hunterbot.config import Config
from hunterbot.ui.main_window import HunterbotWindow
from hunterbot.utils.logger import setup_logging, get_logger
from hunterbot.database.schema import init_database

# Inisialisasi logging
setup_logging()
logger = get_logger(__name__)


def check_config() -> bool:
    """
    Cek konfigurasi sebelum aplikasi jalan.

    Returns:
        True jika config siap, False jika ada yang kurang.
    """
    logger.info("Checking configuration...")

    validation = Config.validate()
    is_ready = validation.get("youtube_api_key", False)

    if not is_ready:
        logger.error("YouTube API key belum diset!")
        return False

    logger.info("Configuration OK")
    return True


def main():
    """
    Main function untuk menjalankan aplikasi.
    """
    logger.info("=" * 50)
    logger.info("MEMULAI HUNTERBOT APLIKASI")
    logger.info("=" * 50)

    # UPDATED: Inisialisasi database sebelum aplikasi jalan
    logger.info("Inisialisasi database...")
    init_database()
    logger.info("Database siap")

    # Cek config
    if not check_config():
        print("\nERROR: YouTube API Key belum diset!")
        print("Silakan set environment variable:")
        print("  Windows: set YOUTUBE_API_KEY=your_api_key")
        print("  Linux/Mac: export YOUTUBE_API_KEY=your_api_key")
        print("\nAtau buat file .env di folder project dan isi:")
        print("  YOUTUBE_API_KEY=your_api_key_here")
        return 1

    # Buat main window
    try:
        app = HunterbotWindow()
        app.mainloop()
        logger.info("Aplikasi ditutup dengan normal")

    except Exception as e:
        logger.exception("Aplikasi error")
        print(f"\nERROR: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
