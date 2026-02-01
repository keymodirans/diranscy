"""
Schema database Hunterbot.

Module ini berisi definisi SQL untuk semua tabel database.
"""

import sqlite3
import logging
from pathlib import Path
from typing import Optional

from hunterbot.config import Config

logger = logging.getLogger(__name__)


# SQL Schema untuk tabel videos (versi dengan Tier 1 validation)
VIDEO_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS videos (
    -- Primary Key
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT UNIQUE NOT NULL,

    -- YouTube Metadata
    title TEXT NOT NULL,
    channel_id TEXT NOT NULL,
    channel_title TEXT NOT NULL,
    subscriber_count INTEGER DEFAULT 0,
    upload_date TEXT NOT NULL,
    upload_days_ago INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    thumbnail_url TEXT NOT NULL,
    description TEXT,

    -- Processing State
    state TEXT DEFAULT 'RAW',
    error_message TEXT,

    -- Hard Filter flags
    passed_min_views BOOLEAN DEFAULT 0,
    passed_max_views_vs_subs BOOLEAN DEFAULT 0,
    passed_upload_age BOOLEAN DEFAULT 0,

    -- Tier 1 Validation fields
    tier1_validated BOOLEAN DEFAULT 0,
    tier1_score REAL DEFAULT 0.0,
    tier1_language_score REAL DEFAULT 0.0,
    tier1_currency_score REAL DEFAULT 0.0,
    tier1_cultural_score REAL DEFAULT 0.0,
    tier1_region_score REAL DEFAULT 0.0,
    tier1_has_exclude BOOLEAN DEFAULT 0,
    channel_location TEXT,

    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Index untuk performa
CREATE INDEX IF NOT EXISTS idx_video_id ON videos(video_id);
CREATE INDEX IF NOT EXISTS idx_state ON videos(state);
CREATE INDEX IF NOT EXISTS idx_views ON videos(views DESC);
CREATE INDEX IF NOT EXISTS idx_upload_days_ago ON videos(upload_days_ago);
CREATE INDEX IF NOT EXISTS idx_tier1_validated ON videos(tier1_validated);
CREATE INDEX IF NOT EXISTS idx_tier1_score ON videos(tier1_score DESC);

-- Trigger untuk auto-update updated_at
CREATE TRIGGER IF NOT EXISTS update_videos_timestamp
AFTER UPDATE ON videos
BEGIN
    UPDATE videos SET updated_at = datetime('now') WHERE id = NEW.id;
END;
"""


def init_database(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Inisialisasi database dan buat tabel jika belum ada.

    Args:
        db_path: Path ke file database. Default dari Config.

    Returns:
        sqlite3.Connection: Koneksi database aktif.
    """
    if db_path is None:
        db_path = Config.DATABASE_PATH

    logger.info(f"Inisialisasi database: {db_path}")

    # Buat koneksi dengan timeout dan WAL mode
    conn = sqlite3.connect(
        db_path,
        timeout=10.0,  # 10 detik timeout
        isolation_level=None  # Autocommit default, bisa override per transaction
    )
    conn.row_factory = sqlite3.Row  # Return baris sebagai objek seperti dict

    # Enable WAL mode untuk better concurrency
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=10000")  # 10 detik
        conn.execute("PRAGMA synchronous=NORMAL")  # Balance speed/safety
        logger.info("WAL mode diaktifkan, timeout=10s")
    except sqlite3.Error as e:
        logger.warning(f"Tidak bisa mengaktifkan WAL mode: {e}")

    # Buat tabel - gunakan executescript untuk multiple statements
    try:
        conn.executescript(VIDEO_TABLE_SCHEMA)
        conn.commit()
        logger.info("Tabel videos berhasil dibuat/terverifikasi")
    except sqlite3.Error as e:
        logger.error(f"Gagal membuat tabel: {e}")
        conn.close()
        raise

    return conn


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Ambil koneksi database yang sudah ada.

    Args:
        db_path: Path ke file database. Default dari Config.

    Returns:
        sqlite3.Connection: Koneksi database aktif.
    """
    if db_path is None:
        db_path = Config.DATABASE_PATH

    conn = sqlite3.connect(
        db_path,
        timeout=10.0,  # 10 detik timeout
        isolation_level=None
    )
    conn.row_factory = sqlite3.Row

    # Set mode WAL untuk setiap koneksi baru
    try:
        conn.execute("PRAGMA busy_timeout=10000")
    except sqlite3.Error:
        pass  # Ignore jika sudah diset

    return conn
