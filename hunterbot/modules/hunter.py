"""
Hunter Module - Modul utama untuk scraping video YouTube.

Module ini mengorchestrasi proses scraping dari YouTube:
1. Search video berdasarkan query
2. Ambil detail video (termasuk description)
3. Ambil channel details (subs + location)
4. Apply hard filter (PRD)
5. Apply Tier 1 validation (baru!)
6. Simpan ke database
"""

import logging
from typing import List, Optional, Callable
from datetime import datetime

from hunterbot.api.youtube_api import YouTubeAPI, YouTubeAPIError, QuotaExceededException
from hunterbot.config import Config
from hunterbot.database.models import Video
from hunterbot.utils.logger import get_logger
from hunterbot.modules.geo_validator import get_validator

logger = get_logger(__name__)


# UPDATED: Filter constants sesuai user requirement
MIN_VIEWS = 5000        # Minimum 5000 views (micro-viral)
MAX_VIEWS = 50000       # Maksimal 50000 views
MAX_DAYS_AGO = 21       # Maksimal 21 hari (3 minggu)
MIN_DAYS_AGO = 0        # Minimal 0 hari
MAX_SUBSCRIBER = 30000  # Maksimal 30000 subscriber (micro-influencer)


def calculate_date_range(max_days_ago: int = 21) -> tuple[str, str]:
    """
    Hitung date range untuk YouTube API filter.

    Args:
        max_days_ago: Maksimal hari ke belakang dari hari ini.

    Returns:
        Tuple (published_after, published_before) dalam ISO 8601 format.
    """
    from datetime import datetime, timezone, timedelta

    now = datetime.now(timezone.utc)
    published_before = now.isoformat()

    # max_days_ago hari ke belakang
    published_after = (now - timedelta(days=max_days_ago)).isoformat()

    return published_after, published_before


class HunterModule:
    """
    Module untuk mengelola proses scraping video YouTube.

    Class ini mengorchestrasi alur lengkap scraping:
    - Search video by query
    - Fetch metadata (video + channel)
    - Apply hard filter
    - Save to database
    """

    def __init__(self, api_key: str = None):
        """
        Inisialisasi Hunter module.

        Args:
            api_key: YouTube Data API key. Default dari Config.
        """
        self.youtube_api = YouTubeAPI(api_key)
        self.progress_callback: Optional[Callable] = None

        # UPDATED: Filter statistics dengan filter baru
        self.stats = {
            "total_scraped": 0,
            "passed_min_views": 0,
            "passed_max_views": 0,
            "passed_upload_age": 0,
            "passed_max_subs": 0,
            "passed_all": 0,
            "failed": 0
        }

        logger.info("Hunter module diinisialisasi")

    def set_progress_callback(self, callback: Callable[[int, int], None]) -> None:
        """
        Set callback function untuk update progress UI.

        Args:
            callback: Function yang menerima (current, total).
        """
        self.progress_callback = callback
        logger.info("Progress callback diatur")

    def _update_progress(self, current: int, total: int, message: str = "") -> None:
        """
        Update progress ke UI.

        Args:
            current: Nomor saat ini.
            total: Total target.
            message: Pesan tambahan.
        """
        if self.progress_callback:
            self.progress_callback(current, total)

        if message:
            logger.info(f"Progress: {current}/{total} - {message}")

    def _apply_hard_filters(
        self,
        video_data: dict,
        subscriber_count: int
    ) -> tuple[bool, dict]:
        """
        Apply hard filter sesuai user requirement.

        UPDATED: Micro-influencer hunting (5k-50k views, max 30k subs)

        Args:
            video_data: Video metadata dari YouTube API.
            subscriber_count: Channel subscriber count.

        Returns:
            Tuple (passed_all, filter_results).
        """
        views = video_data.get("views", 0)
        upload_date = video_data.get("upload_date", "")

        # Calculate days ago
        days_ago = self.youtube_api.calculate_days_ago(upload_date)

        # UPDATED: Filter 1 - Views range 5000 - 50000
        passed_min_views = views >= MIN_VIEWS      # 5000 views minimum
        passed_max_views = views <= MAX_VIEWS      # 50000 views maximum

        # UPDATED: Filter 2 - Upload age 0-21 days
        passed_upload_age = days_ago <= MAX_DAYS_AGO

        # UPDATED: Filter 3 - Max subscriber 30000 (micro-influencer)
        passed_max_subs = subscriber_count <= MAX_SUBSCRIBER

        # All filters must pass
        passed_all = (
            passed_min_views and
            passed_max_views and
            passed_upload_age and
            passed_max_subs
        )

        filter_results = {
            "passed_min_views": passed_min_views,
            "passed_max_views": passed_max_views,
            "passed_upload_age": passed_upload_age,
            "passed_max_subs": passed_max_subs,
            "passed_all": passed_all,
            "days_ago": days_ago,
        }

        return passed_all, filter_results

    def scrape_videos(
        self,
        query: str,
        target_count: int = None,
        max_videos_per_search: int = 50
    ) -> dict:
        """
        Scraping video dari YouTube dengan hard filter PRD.

        Args:
            query: Kata kunci pencarian.
            target_count: Target jumlah video (default dari config).
            max_videos_per_search: Maksimal video per search (default 50).

        Returns:
            Dict dengan statistik scraping hasil.

        Raises:
            ValueError: Jika parameter tidak valid.
            YouTubeAPIError: Jika scraping gagal.
        """
        # UPDATED: Reset statistics dengan filter baru
        self.stats = {
            "total_scraped": 0,
            "passed_min_views": 0,
            "passed_max_views": 0,
            "passed_upload_age": 0,
            "passed_max_subs": 0,
            "passed_all": 0,
            "failed": 0
        }

        if target_count is None:
            target_count = Config.TARGET_VIDEO_COUNT

        if target_count <= 0:
            raise ValueError("target_count harus lebih dari 0")

        # UPDATED: Hapus semua data lama sebelum scraping mulai
        from hunterbot.database.models import Video
        deleted_count = Video.delete_all()
        if deleted_count > 0:
            logger.info(f"Database dibersihkan: {deleted_count} video lama dihapus")
        else:
            logger.info("Database kosong, siap untuk scraping baru")

        logger.info(f"Memulai scraping dengan filter: query='{query}', target={target_count}")
        logger.info(f"Filter: Views {MIN_VIEWS}-{MAX_VIEWS}, Subs max {MAX_SUBSCRIBER}, {MIN_DAYS_AGO}-{MAX_DAYS_AGO} days")

        # Hitung date range untuk API filter
        published_after, published_before = calculate_date_range(MAX_DAYS_AGO)
        logger.info(f"Date range: {published_after} s/d {published_before}")

        video_ids_seen = set()

        try:
            # Search batch 1 dengan date range filter
            self._update_progress(0, target_count, "Mencari video...")

            video_ids, next_page = self.youtube_api.search_videos(
                query=query,
                max_results=min(max_videos_per_search, target_count),
                published_after=published_after,
                published_before=published_before
            )

            video_ids_seen.update(video_ids)

            # Pagination kalau butuh lebih banyak video (fetch lebih banyak karena akan difilter)
            page_count = 1
            target_with_buffer = target_count * 3  # Fetch 3× lebih banyak untuk buffer filter

            while len(video_ids_seen) < target_with_buffer and next_page:
                page_count += 1
                logger.info(f"Fetch halaman {page_count}")

                video_ids, next_page = self.youtube_api.search_videos(
                    query=query,
                    max_results=min(max_videos_per_search, target_with_buffer - len(video_ids_seen)),
                    page_token=next_page,
                    published_after=published_after,
                    published_before=published_before
                )

                video_ids_seen.update(video_ids)

                if not video_ids:
                    logger.warning("Tidak ada video tambahan di halaman ini")
                    break

            # Ambil detail video
            unique_video_ids = list(video_ids_seen)[:target_with_buffer]
            logger.info(f"Total {len(unique_video_ids)} video akan diproses")

            self._update_progress(0, len(unique_video_ids), "Ambil detail video...")

            video_details = self.youtube_api.get_video_details(unique_video_ids)
            self.stats["total_scraped"] = len(video_details)

            # Fetch channel details untuk subscriber count
            self._update_progress(0, len(video_details), "Ambil channel details...")

            unique_channel_ids = list(set([v["channel_id"] for v in video_details]))
            channel_details = self.youtube_api.get_channel_details(unique_channel_ids)

            # Apply filter dan simpan yang lulus
            self._update_progress(0, len(video_details), "Apply filter & simpan...")

            # Get Tier 1 validator
            validator = get_validator()

            saved_count = 0
            tier1_passed = 0

            for idx, video_data in enumerate(video_details):
                try:
                    channel_id = video_data["channel_id"]
                    channel_data = channel_details.get(channel_id, {})
                    subscriber_count = channel_data.get("subscriber_count", 0)
                    channel_location = channel_data.get("location", "")
                    views = video_data.get("views", 0)
                    video_id = video_data.get("video_id", "")

                    # UPDATED: Log progress per video
                    logger.info(f"[{idx+1}/{len(video_details)}] Processing: {video_id} | {views:,} views | {subscriber_count:,} subs")

                    # Apply hard filter
                    passed_hard, filter_results = self._apply_hard_filters(video_data, subscriber_count)

                    # UPDATED: Update statistics dengan filter baru
                    if filter_results["passed_min_views"]:
                        self.stats["passed_min_views"] += 1
                    if filter_results["passed_max_views"]:
                        self.stats["passed_max_views"] += 1
                    if filter_results["passed_upload_age"]:
                        self.stats["passed_upload_age"] += 1
                    if filter_results["passed_max_subs"]:
                        self.stats["passed_max_subs"] += 1

                    if passed_hard:
                        self.stats["passed_all"] += 1

                        # UPDATED: Log lulus hard filter
                        logger.info(f"[{idx+1}/{len(video_details)}] ✓ Hard filter PASS → Tier1 validating...")

                        # Apply Tier 1 validation (hanya yang lulus hard filter)
                        title = video_data.get("title", "")
                        description = video_data.get("description", "")
                        tier1_result = validator.validate_tier1(title, description, channel_location)

                        # Simpan hanya yang lulus Tier 1
                        if tier1_result["passed"]:
                            tier1_passed += 1

                            # UPDATED: Log lulus Tier 1
                            logger.info(f"[{idx+1}/{len(video_details)}] ✓✓ Tier1 PASS (score: {tier1_result['score']:.2f}) → SAVING...")

                            video = Video(
                                video_id=video_data["video_id"],
                                title=video_data["title"],
                                channel_id=video_data["channel_id"],
                                channel_title=video_data["channel_title"],
                                subscriber_count=subscriber_count,
                                upload_date=video_data["upload_date"],
                                upload_days_ago=filter_results["days_ago"],
                                views=video_data["views"],
                                likes=video_data.get("likes", 0),
                                thumbnail_url=video_data["thumbnail_url"],
                                description=description,
                                state=Video.STATE_SCRAPED,
                                # UPDATED: Hapus field lama passed_max_views_vs_subs
                                passed_min_views=True,
                                passed_max_views=True,
                                passed_upload_age=True,
                                # Tier 1 fields
                                tier1_validated=True,
                                tier1_score=tier1_result["score"],
                                tier1_language_score=tier1_result["scores"]["language"],
                                tier1_currency_score=tier1_result["scores"]["currency"],
                                tier1_cultural_score=tier1_result["scores"]["cultural"],
                                tier1_region_score=tier1_result["scores"]["region"],
                                tier1_has_exclude=tier1_result["has_exclude_patterns"],
                                channel_location=channel_location
                            )

                            if video.save():
                                saved_count += 1
                                logger.info(f"[{idx+1}/{len(video_details)}] ✓✓ SAVED: {video_data['video_id']}")
                            else:
                                logger.warning(f"[{idx+1}/{len(video_details)}] ✗ FAILED TO SAVE: {video_data['video_id']}")
                        else:
                            self.stats["failed"] += 1
                            logger.info(f"[{idx+1}/{len(video_details)}] ✗ Tier1 FAIL (score: {tier1_result['score']:.2f})")
                    else:
                        self.stats["failed"] += 1
                        # UPDATED: Log gagal hard filter dengan alasan
                        fail_reason = []
                        if not filter_results["passed_min_views"]:
                            fail_reason.append(f"views={views}<{MIN_VIEWS}")
                        if not filter_results["passed_max_views"]:
                            fail_reason.append(f"views={views}>{MAX_VIEWS}")
                        if not filter_results["passed_upload_age"]:
                            fail_reason.append(f"age={filter_results['days_ago']}d>{MAX_DAYS_AGO}")
                        if not filter_results["passed_max_subs"]:
                            fail_reason.append(f"subs={subscriber_count}>{MAX_SUBSCRIBER}")
                        reason_str = ", ".join(fail_reason)
                        logger.info(f"[{idx+1}/{len(video_details)}] ✗ Hard filter FAIL: {reason_str}")

                    self._update_progress(idx + 1, len(video_details))

                    # Rate limiting
                    if idx < len(video_details) - 1:
                        self.youtube_api.rate_limit()

                except Exception as e:
                    logger.error(f"Gagal memproses video {video_data['video_id']}: {e}")
                    self.stats["failed"] += 1
                    continue

        except QuotaExceededException:
            logger.error("YouTube API quota habis. Gunakan API key lain besok.")
            raise

        except YouTubeAPIError as e:
            logger.error(f"Scraping gagal: {e}")
            raise

        except Exception as e:
            logger.exception(f"Error tidak terduga saat scraping: {e}")
            raise

        # UPDATED: Log statistik dengan filter baru
        logger.info("=" * 50)
        logger.info("SCRAPING SELESAI - STATISTIK")
        logger.info("=" * 50)
        logger.info(f"Total discraping: {self.stats['total_scraped']}")
        logger.info(f"Lulus min views ({MIN_VIEWS}+): {self.stats['passed_min_views']}")
        logger.info(f"Lulus max views ({MAX_VIEWS}-): {self.stats['passed_max_views']}")
        logger.info(f"Lulus upload age (0-{MAX_DAYS_AGO} days): {self.stats['passed_upload_age']}")
        logger.info(f"Lulus max subs ({MAX_SUBSCRIBER}-): {self.stats['passed_max_subs']}")
        logger.info(f"Lulus SEMUA filter: {self.stats['passed_all']}")
        logger.info(f"Lulus Tier 1: {tier1_passed}")
        logger.info(f"Gagal/Tidak lulus: {self.stats['failed']}")
        logger.info("=" * 50)

        return self.stats

    def scrape_videos_simple(self, query: str, count: int = 10) -> List[dict]:
        """
        Metode simple untuk scraping (untuk testing).

        Args:
            query: Kata kunci pencarian.
            count: Jumlah video yang diinginkan (default 10).

        Returns:
            List of video dictionaries.
        """
        logger.info(f"Scraping simple: query='{query}', count={count}")

        try:
            # Search
            video_ids, _ = self.youtube_api.search_videos(query, max_results=count)

            # Get details
            videos = self.youtube_api.get_video_details(video_ids)

            return videos

        except YouTubeAPIError as e:
            logger.error(f"Scraping simple gagal: {e}")
            return []
