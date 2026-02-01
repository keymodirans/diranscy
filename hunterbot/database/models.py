"""
Model database Hunterbot.

Module ini berisi kelas model untuk interaksi dengan tabel database.
"""

import sqlite3
import logging
import time
from typing import Optional, List, Dict, Any
from datetime import datetime

from hunterbot.database.schema import get_connection

logger = logging.getLogger(__name__)


def retry_on_locked(func, max_retries=3):
    """
    Decorator untuk retry function jika database locked.

    Args:
        func: Function yang akan di-retry.
        max_retries: Maksimal percobaan ulang.

    Returns:
        Wrapper function.
    """
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except sqlite3.OperationalError as e:
                if "locked" in str(e).lower() and attempt < max_retries - 1:
                    wait_time = 0.5 * (2 ** attempt)  # 0.5s, 1s, 2s
                    logger.warning(f"Database locked, retry {attempt + 1}/{max_retries} dalam {wait_time}s")
                    time.sleep(wait_time)
                    continue
                raise
        return wrapper


class Video:
    """
    Model untuk tabel videos.

    Class ini menyediakan method untuk CRUD operasi pada video records.
    """

    # State constants
    STATE_RAW = "RAW"
    STATE_SCRAPED = "SCRAPED"
    STATE_PROCESSED = "PROCESSED"
    STATE_FAILED = "FAILED"

    def __init__(self, **kwargs):
        """
        Inisialisasi objek Video.

        Args:
            **kwargs: Field-value pairs untuk kolom database.
        """
        self.id = kwargs.get("id")
        self.video_id = kwargs.get("video_id")
        self.title = kwargs.get("title")
        self.channel_id = kwargs.get("channel_id")
        self.channel_title = kwargs.get("channel_title")
        self.subscriber_count = kwargs.get("subscriber_count", 0)
        self.upload_date = kwargs.get("upload_date")
        self.upload_days_ago = kwargs.get("upload_days_ago", 0)
        self.views = kwargs.get("views", 0)
        self.thumbnail_url = kwargs.get("thumbnail_url")
        self.description = kwargs.get("description", "")
        self.state = kwargs.get("state", self.STATE_RAW)
        self.error_message = kwargs.get("error_message", "")
        self.passed_min_views = kwargs.get("passed_min_views", False)
        self.passed_max_views_vs_subs = kwargs.get("passed_max_views_vs_subs", False)
        self.passed_upload_age = kwargs.get("passed_upload_age", False)

        # Tier 1 validation fields
        self.tier1_validated = kwargs.get("tier1_validated", False)
        self.tier1_score = kwargs.get("tier1_score", 0.0)
        self.tier1_language_score = kwargs.get("tier1_language_score", 0.0)
        self.tier1_currency_score = kwargs.get("tier1_currency_score", 0.0)
        self.tier1_cultural_score = kwargs.get("tier1_cultural_score", 0.0)
        self.tier1_region_score = kwargs.get("tier1_region_score", 0.0)
        self.tier1_has_exclude = kwargs.get("tier1_has_exclude", False)
        self.channel_location = kwargs.get("channel_location", "")

        # Additional metrics
        self.likes = kwargs.get("likes", 0)

        self.created_at = kwargs.get("created_at")
        self.updated_at = kwargs.get("updated_at")

    @classmethod
    def from_db_row(cls, row: sqlite3.Row) -> "Video":
        """
        Buat objek Video dari database row.

        Args:
            row: sqlite3.Row object.

        Returns:
            Video instance.
        """
        return cls(**dict(row))

    def to_dict(self) -> Dict[str, Any]:
        """
        Konversi objek ke dictionary.

        Returns:
            Dict representation dari objek.
        """
        return {
            "id": self.id,
            "video_id": self.video_id,
            "title": self.title,
            "channel_id": self.channel_id,
            "channel_title": self.channel_title,
            "subscriber_count": self.subscriber_count,
            "upload_date": self.upload_date,
            "upload_days_ago": self.upload_days_ago,
            "views": self.views,
            "likes": self.likes,
            "thumbnail_url": self.thumbnail_url,
            "description": self.description,
            "state": self.state,
            "error_message": self.error_message,
            "passed_min_views": self.passed_min_views,
            "passed_max_views_vs_subs": self.passed_max_views_vs_subs,
            "passed_upload_age": self.passed_upload_age,
            "tier1_validated": self.tier1_validated,
            "tier1_score": self.tier1_score,
            "tier1_language_score": self.tier1_language_score,
            "tier1_currency_score": self.tier1_currency_score,
            "tier1_cultural_score": self.tier1_cultural_score,
            "tier1_region_score": self.tier1_region_score,
            "tier1_has_exclude": self.tier1_has_exclude,
            "channel_location": self.channel_location,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @retry_on_locked
    def save(self) -> bool:
        """
        Simpan atau update video ke database.

        Dengan retry logic jika database locked (exponential backoff).

        Returns:
            bool: True jika berhasil, False jika gagal.
        """
        conn = None
        try:
            conn = get_connection()
            cursor = conn.cursor()

            if self.id is None:
                # Insert baru dengan IGNORE untuk skip duplicate
                cursor.execute("""
                    INSERT OR IGNORE INTO videos (
                        video_id, title, channel_id, channel_title, subscriber_count,
                        upload_date, upload_days_ago, views, likes, thumbnail_url, description,
                        state, error_message, passed_min_views, passed_max_views_vs_subs, passed_upload_age,
                        tier1_validated, tier1_score, tier1_language_score, tier1_currency_score,
                        tier1_cultural_score, tier1_region_score, tier1_has_exclude, channel_location
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.video_id,
                    self.title,
                    self.channel_id,
                    self.channel_title,
                    self.subscriber_count,
                    self.upload_date,
                    self.upload_days_ago,
                    self.views,
                    self.likes,
                    self.thumbnail_url,
                    self.description,
                    self.state,
                    self.error_message,
                    1 if self.passed_min_views else 0,
                    1 if self.passed_max_views_vs_subs else 0,
                    1 if self.passed_upload_age else 0,
                    1 if self.tier1_validated else 0,
                    self.tier1_score,
                    self.tier1_language_score,
                    self.tier1_currency_score,
                    self.tier1_cultural_score,
                    self.tier1_region_score,
                    1 if self.tier1_has_exclude else 0,
                    self.channel_location
                ))

                # Cek apakah insert berhasil atau di-skip karena duplicate
                if cursor.rowcount > 0:
                    self.id = cursor.lastrowid
                    logger.info(f"Video baru ditambahkan: {self.video_id}")
                else:
                    logger.debug(f"Video {self.video_id} sudah ada, di-skip")
            else:
                # Update existing
                cursor.execute("""
                    UPDATE videos SET
                        title = ?, channel_id = ?, channel_title = ?, subscriber_count = ?,
                        upload_date = ?, upload_days_ago = ?, views = ?, likes = ?, thumbnail_url = ?,
                        description = ?, state = ?, error_message = ?, passed_min_views = ?,
                        passed_max_views_vs_subs = ?, passed_upload_age = ?,
                        tier1_validated = ?, tier1_score = ?, tier1_language_score = ?,
                        tier1_currency_score = ?, tier1_cultural_score = ?, tier1_region_score = ?,
                        tier1_has_exclude = ?, channel_location = ?
                    WHERE id = ?
                """, (
                    self.title,
                    self.channel_id,
                    self.channel_title,
                    self.subscriber_count,
                    self.upload_date,
                    self.upload_days_ago,
                    self.views,
                    self.likes,
                    self.thumbnail_url,
                    self.description,
                    self.state,
                    self.error_message,
                    1 if self.passed_min_views else 0,
                    1 if self.passed_max_views_vs_subs else 0,
                    1 if self.passed_upload_age else 0,
                    1 if self.tier1_validated else 0,
                    self.tier1_score,
                    self.tier1_language_score,
                    self.tier1_currency_score,
                    self.tier1_cultural_score,
                    self.tier1_region_score,
                    1 if self.tier1_has_exclude else 0,
                    self.channel_location,
                    self.id
                ))
                logger.info(f"Video diperbarui: {self.id}")

            conn.commit()
            return True

        except sqlite3.Error as e:
            logger.error(f"Gagal menyimpan video {self.video_id}: {e}")
            return False
        finally:
            if conn:
                conn.close()

    @classmethod
    def get_by_video_id(cls, video_id: str) -> Optional["Video"]:
        """
        Ambil video berdasarkan video_id.

        Args:
            video_id: YouTube video ID (11 karakter).

        Returns:
            Video object atau None jika tidak ditemukan.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM videos WHERE video_id = ?
            """, (video_id,))

            row = cursor.fetchone()
            conn.close()

            if row:
                return cls.from_db_row(row)
            return None

        except sqlite3.Error as e:
            logger.error(f"Gagal mengambil video {video_id}: {e}")
            return None

    @classmethod
    def get_all(cls, limit: Optional[int] = None) -> List["Video"]:
        """
        Ambil semua video dari database.

        Args:
            limit: Maksimal jumlah video. Default None (semua).

        Returns:
            List of Video objects.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            query = "SELECT * FROM videos ORDER BY views DESC"
            if limit:
                query += f" LIMIT {limit}"

            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            return [cls.from_db_row(row) for row in rows]

        except sqlite3.Error as e:
            logger.error(f"Gagal mengambil daftar video: {e}")
            return []

    @classmethod
    def count(cls) -> int:
        """
        Hitung total video dalam database.

        Returns:
            Jumlah video dalam database.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM videos")
            count = cursor.fetchone()[0]
            conn.close()

            return count

        except sqlite3.Error as e:
            logger.error(f"Gagal menghitung video: {e}")
            return 0

    @classmethod
    def delete_all(cls) -> int:
        """
        Hapus semua video dari database.

        Returns:
            Jumlah video yang dihapus.
        """
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM videos")
            count = cursor.rowcount
            conn.commit()
            conn.close()

            logger.info(f"Semua video dihapus: {count} record")
            return count

        except sqlite3.Error as e:
            logger.error(f"Gagal menghapus video: {e}")
            return 0

    # Computed properties untuk UI display
    @property
    def upload_date_only(self) -> str:
        """Tanggal upload saja (YYYY-MM-DD)."""
        if not self.upload_date:
            return ""
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(self.upload_date.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d")
        except:
            return self.upload_date[:10] if len(self.upload_date) >= 10 else ""

    @property
    def upload_time_only(self) -> str:
        """Waktu upload saja (HH:MM)."""
        if not self.upload_date:
            return ""
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(self.upload_date.replace("Z", "+00:00"))
            return dt.strftime("%H:%M")
        except:
            return ""

    @property
    def views_formatted(self) -> str:
        """Views dalam format ribuan (1K, 1M, etc.)."""
        views = self.views or 0
        if views >= 1000000:
            return f"{views / 1000000:.1f}M"
        elif views >= 1000:
            return f"{views / 1000:.1f}K"
        return str(views)

    @property
    def subscribers_formatted(self) -> str:
        """Subscribers dalam format ribuan."""
        subs = self.subscriber_count or 0
        if subs >= 1000000:
            return f"{subs / 1000000:.1f}M"
        elif subs >= 1000:
            return f"{subs / 1000:.1f}K"
        return str(subs)

    @property
    def vph(self) -> float:
        """
        Views Per Hour - VPH.

        Hitungan: views / (days_ago × 24)
        """
        if self.upload_days_ago and self.upload_days_ago > 0:
            hours = self.upload_days_ago * 24
            return round(self.views / hours, 2) if self.views else 0
        return 0.0

    @property
    def engagement_rate(self) -> float:
        """
        Engagement Rate % = (likes / views) × 100.

        Returns 0.0 jika likes = 0.
        """
        if self.views and self.views > 0:
            return round((self.likes / self.views) * 100, 2)
        return 0.0

    @property
    def channel_url(self) -> str:
        """URL channel YouTube."""
        return f"https://www.youtube.com/channel/{self.channel_id}"

    @property
    def country_name(self) -> str:
        """Nama country dari channel location code."""
        if not self.channel_location:
            return "Unknown"

        country_map = {
            "US": "United States",
            "GB": "United Kingdom",
            "CA": "Canada",
            "AU": "Australia",
            "IN": "India",
            "ID": "Indonesia",
            "SG": "Singapore",
            "MY": "Malaysia",
            "PH": "Philippines",
            "TH": "Thailand",
            "VN": "Vietnam",
            "DE": "Germany",
            "FR": "France",
            "IT": "Italy",
            "ES": "Spain",
            "NL": "Netherlands",
            "BR": "Brazil",
            "MX": "Mexico",
            "JP": "Japan",
            "KR": "South Korea",
            "NZ": "New Zealand",
        }
        return country_map.get(self.channel_location.upper(), self.channel_location)
