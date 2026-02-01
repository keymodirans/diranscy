"""
Konfigurasi aplikasi Hunterbot.

Module ini berisi semua konfigurasi global untuk aplikasi.
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables dari .env file
ENV_FILE = Path(__file__).parent.parent / ".env"
load_dotenv(ENV_FILE)

# Base paths
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
EXPORTS_DIR = BASE_DIR / "exports"
DATABASE_PATH = BASE_DIR / "hunterbot.db"

# Directories setup
LOGS_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)


class Config:
    """Konfigurasi global aplikasi."""

    # Database
    DATABASE_PATH: str = str(DATABASE_PATH)
    DATABASE_BACKUP_DIR: Path = BASE_DIR / "backups"
    DATABASE_BACKUP_DIR.mkdir(exist_ok=True)

    # API Keys (dari environment variables)
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    DEEPGRAM_API_KEY: str = os.getenv("DEEPGRAM_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # Scraping settings
    TARGET_VIDEO_COUNT: int = 100  # MVP: 100 videos
    MAX_RESULTS_PER_REQUEST: int = 50
    REGION_CODE: str = "US"
    RELEVANCE_LANGUAGE: str = "en"

    # Rate limiting (seconds)
    YOUTUBE_RATE_LIMIT: float = 2.0
    DEEPGRAM_RATE_LIMIT: float = 2.0
    GEMINI_RATE_LIMIT: float = 1.0

    # UI Settings
    WINDOW_WIDTH: int = 800
    WINDOW_HEIGHT: int = 600
    WINDOW_TITLE: str = "Hunterbot v1.0 MVP"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def validate(cls) -> Dict[str, bool]:
        """
        Validasi konfigurasi aplikasi.

        Returns:
            Dict dengan status validasi setiap komponen.
        """
        validation_result = {
            "youtube_api_key": bool(cls.YOUTUBE_API_KEY),
            "deepgram_api_key": bool(cls.DEEPGRAM_API_KEY),  # Optional untuk MVP
            "gemini_api_key": bool(cls.GEMINI_API_KEY),      # Optional untuk MVP
            "database_path": True,  # Akan dibuat otomatis
        }

        return validation_result

    @classmethod
    def is_mvp_ready(cls) -> bool:
        """
        Cek apakah konfigurasi sudah siap untuk MVP.

        MVP hanya butuh YouTube API key.
        """
        return bool(cls.YOUTUBE_API_KEY)
