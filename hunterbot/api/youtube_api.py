"""
YouTube Data API v3 Client.

Module ini berisi fungsi untuk mengambil data dari YouTube Data API.
"""

import logging
import time
import requests
from typing import List, Tuple, Optional, Dict, Any

from hunterbot.config import Config
from hunterbot.utils.logger import get_logger

logger = get_logger(__name__)


class YouTubeAPIError(Exception):
    """Exception untuk error YouTube API."""
    pass


class QuotaExceededException(YouTubeAPIError):
    """Exception ketika quota YouTube API habis."""
    pass


class YouTubeAPI:
    """
    Client untuk YouTube Data API v3.

    Class ini menyediakan method untuk:
    - Search video by query
    - Get video details
    - Get channel details
    """

    def __init__(self, api_key: str = None):
        """
        Inisialisasi YouTube API client.

        Args:
            api_key: YouTube Data API key. Default dari Config.
        """
        if api_key is None:
            api_key = Config.YOUTUBE_API_KEY

        if not api_key:
            raise ValueError("YouTube API key tidak boleh kosong")

        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.session = requests.Session()

        logger.info("YouTube API client diinisialisasi")

    def search_videos(
        self,
        query: str,
        max_results: int = 50,
        region_code: str = None,
        page_token: str = None,
        published_after: str = None,
        published_before: str = None
    ) -> Tuple[List[str], Optional[str]]:
        """
        Cari video di YouTube berdasarkan query dengan opsi date range filter.

        Args:
            query: Kata kunci pencarian.
            max_results: Maksimal hasil per request (max 50).
            region_code: Kode negara (default US).
            page_token: Token untuk pagination (default None).
            published_after: ISO 8601 format untuk tanggal awal (2024-01-01T00:00:00Z).
            published_before: ISO 8601 format untuk tanggal akhir (2024-12-31T23:59:59Z).

        Returns:
            Tuple (list of video_ids, next_page_token).

        Raises:
            YouTubeAPIError: Jika request gagal.
        """
        if region_code is None:
            region_code = Config.REGION_CODE

        logger.info(f"Mencari video: query='{query}', max_results={max_results}, page_token={page_token}")

        params = {
            "key": self.api_key,
            "part": "snippet",
            "q": query,
            "type": "video",
            "order": "viewCount",
            "maxResults": min(max_results, 50),
            "regionCode": region_code,
            "relevanceLanguage": Config.RELEVANCE_LANGUAGE,
            "videoEmbeddable": "true"
        }

        # Tambah page_token jika ada
        if page_token:
            params["pageToken"] = page_token

        # Tambah date range filter jika ada
        if published_after:
            params["publishedAfter"] = published_after
            logger.debug(f"Filter publishedAfter: {published_after}")

        if published_before:
            params["publishedBefore"] = published_before
            logger.debug(f"Filter publishedBefore: {published_before}")

        try:
            response = self.session.get(
                f"{self.base_url}/search",
                params=params,
                timeout=30
            )
            response.raise_for_status()

            data = response.json()

            # Cek error dari YouTube
            if "error" in data:
                self._handle_api_error(data["error"])

            # Ekstrak video IDs
            video_ids = [
                item["id"]["videoId"]
                for item in data.get("items", [])
            ]

            next_page_token = data.get("nextPageToken")

            logger.info(f"Ditemukan {len(video_ids)} video IDs")

            return video_ids, next_page_token

        except requests.exceptions.RequestException as e:
            logger.error(f"Request gagal: {e}")
            raise YouTubeAPIError(f"Gagal menghubungi YouTube API: {e}")

    def get_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Ambil detail video secara batch dengan auto-batching.

        Args:
            video_ids: List video ID (lebih dari 50 akan di-batch otomatis).

        Returns:
            List of video metadata dictionaries.

        Raises:
            YouTubeAPIError: Jika request gagal.
        """
        all_videos = []

        # Auto-batching: pecah jadi chunks of 50
        for i in range(0, len(video_ids), 50):
            chunk = video_ids[i:i + 50]
            logger.info(f"Mengambil detail {len(chunk)} videos (batch {i // 50 + 1})")

            params = {
                "key": self.api_key,
                "part": "snippet,statistics",
                "id": ",".join(chunk)
            }

            try:
                response = self.session.get(
                    f"{self.base_url}/videos",
                    params=params,
                    timeout=30
                )
                response.raise_for_status()

                data = response.json()

                if "error" in data:
                    self._handle_api_error(data["error"])

                # Parse video details
                for item in data.get("items", []):
                    video = {
                        "video_id": item["id"],
                        "title": item["snippet"]["title"],
                        "channel_id": item["snippet"]["channelId"],
                        "channel_title": item["snippet"]["channelTitle"],
                        "upload_date": item["snippet"]["publishedAt"],
                        "views": int(item["statistics"].get("viewCount", 0)),
                        "description": item["snippet"].get("description", ""),
                        "thumbnail_url": self._extract_thumbnail(
                            item["snippet"]["thumbnails"]
                        )
                    }
                    all_videos.append(video)

                logger.info(f"Batch {i // 50 + 1} selesai, total {len(all_videos)} videos")

                # Rate limiting antar batch
                if i + 50 < len(video_ids):
                    self.rate_limit()

            except requests.exceptions.RequestException as e:
                logger.error(f"Request gagal pada batch {i // 50 + 1}: {e}")
                raise YouTubeAPIError(f"Gagal mengambil detail video: {e}")

        logger.info(f"Berhasil mengambil detail {len(all_videos)} videos (total)")

        return all_videos

    def get_channel_details(self, channel_ids: List[str]) -> Dict[str, dict]:
        """
        Ambil channel details (subs + location) secara batch dengan auto-batching.

        Args:
            channel_ids: List channel ID (lebih dari 50 akan di-batch otomatis).

        Returns:
            Dict mapping channel_id ke {subscriber_count, location}.

        Raises:
            YouTubeAPIError: Jika request gagal.
        """
        all_channel_data = {}

        # Auto-batching: pecah jadi chunks of 50
        for i in range(0, len(channel_ids), 50):
            chunk = channel_ids[i:i + 50]
            logger.info(f"Mengambil detail {len(chunk)} channels (batch {i // 50 + 1})")

            params = {
                "key": self.api_key,
                "part": "statistics,snippet",
                "id": ",".join(chunk)
            }

            try:
                response = self.session.get(
                    f"{self.base_url}/channels",
                    params=params,
                    timeout=30
                )
                response.raise_for_status()

                data = response.json()

                if "error" in data:
                    self._handle_api_error(data["error"])

                # Parse channel details
                for item in data.get("items", []):
                    channel_id = item["id"]
                    subscriber_count = int(item["statistics"].get("subscriberCount", 0))
                    # Get location from snippet (country)
                    location = item["snippet"].get("country", "")
                    # Or from localized title/description
                    if not location:
                        location = item["snippet"].get("localized", {}).get("country", "")

                    all_channel_data[channel_id] = {
                        "subscriber_count": subscriber_count,
                        "location": location
                    }

                logger.info(f"Batch {i // 50 + 1} selesai, total {len(all_channel_data)} channels")

                # Rate limiting antar batch
                if i + 50 < len(channel_ids):
                    self.rate_limit()

            except requests.exceptions.RequestException as e:
                logger.error(f"Request gagal pada batch {i // 50 + 1}: {e}")
                raise YouTubeAPIError(f"Gagal mengambil channel details: {e}")

        logger.info(f"Berhasil mengambil {len(all_channel_data)} channel details (total)")

        return all_channel_data

    def calculate_days_ago(self, upload_date_str: str) -> int:
        """
        Hitung berapa hari sejak video diupload.

        Args:
            upload_date_str: ISO 8601 date string dari YouTube API.

        Returns:
            Jumlah hari sejak upload.
        """
        try:
            from datetime import datetime, timezone

            # Parse ISO 8601 format: 2024-01-15T10:30:00Z
            upload_date = datetime.fromisoformat(upload_date_str.replace("Z", "+00:00"))

            # Convert to UTC if naive
            if upload_date.tzinfo is None:
                upload_date = upload_date.replace(tzinfo=timezone.utc)

            # Get current time in UTC
            now = datetime.now(timezone.utc)

            # Calculate difference
            delta = now - upload_date
            days_ago = delta.days

            return days_ago

        except Exception as e:
            logger.warning(f"Gagal hitung hari dari {upload_date_str}: {e}")
            return 0

    def _extract_thumbnail(self, thumbnails: Dict[str, Any]) -> str:
        """
        Ekstrak URL thumbnail dengan kualitas terbaik.

        Args:
            thumbnails: Thumbnails object dari YouTube API.

        Returns:
            URL thumbnail terbaik.
        """
        quality_priority = ["maxres", "standard", "high", "medium", "default"]

        for quality in quality_priority:
            if quality in thumbnails:
                return thumbnails[quality]["url"]

        # Fallback
        return thumbnails.get("default", {}).get("url", "")

    def _handle_api_error(self, error_data: Dict[str, Any]) -> None:
        """
        Handle error response dari YouTube API.

        Args:
            error_data: Error object dari YouTube API response.

        Raises:
            QuotaExceededException: Jika quota habis.
            YouTubeAPIError: Untuk error lainnya.
        """
        reason = error_data.get("errors", [{}])[0].get("reason", "unknown")

        if reason == "quotaExceeded":
            logger.error("YouTube API quota habis")
            raise QuotaExceededException("YouTube API quota habis")

        logger.error(f"YouTube API error: {reason}")
        raise YouTubeAPIError(f"YouTube API error: {reason}")

    def rate_limit(self, delay: float = None) -> None:
        """
        Apply rate limiting dengan delay.

        Args:
            delay: Delay dalam detik. Default dari config.
        """
        if delay is None:
            delay = Config.YOUTUBE_RATE_LIMIT

        logger.debug(f"Rate limiting: {delay} detik")
        time.sleep(delay)
