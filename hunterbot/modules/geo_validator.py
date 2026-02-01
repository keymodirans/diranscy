"""
Geo-Validator Module - Tier 1 Audience Validation.

Module ini memvalidasi apakah video target audience adalah US (United States).
Ini untuk exclude video dari non-US creators yang menggunakan VPN.

Tier 1 Components:
- Language (40%): English detection
- Currency (30%): USD/ Dollar presence
- Cultural (20%): US/Western context
- Region (10%): Channel location = US
"""

import re
import logging
from typing import Dict, Any, Optional

try:
    from langdetect import detect, LangDetectException
except ImportError:
    detect = None

from hunterbot.utils.logger import get_logger

logger = get_logger(__name__)


class GeoValidator:
    """
    Validator untuk Tier 1 audience (US).

    Validasi multi-factor untuk memastikan video benar-bear
    target audience US, bukan non-US creator dengan VPN.
    """

    # US/Western cultural keywords
    US_CULTURAL_KEYWORDS = [
        "american", "usa", "united states", "us culture",
        "western", "america", "us history", "us politics",
        "us election", "us economy", "hollywood", "nyc",
        "los angeles", "chicago", "texas", "california",
        "us constitution", "us military", "us news"
    ]

    # Non-US keywords untuk exclude (India, Pakistan, dll)
    EXCLUDE_REGIONS = [
        "indian", "india", "bollywood", "desi", "hindu",
        "pakistan", "paki", "karachi", "mumbai", "delhi",
        "bangalore", "hyderabad", "chennai", "srilanka",
        "nepal", "bangla", "hindi", "telugu", "tamil",
        "urdu", "cricket india", "ipl", "bhai", "jiyo"
    ]

    # Currency patterns
    USD_PATTERNS = [
        r'\$\d+',           # $100, $50, etc
        r'USD',             # USD
        r'dollar',          # dollar
        r' dollars?\b',     # dollar, dollars
    ]

    # INR patterns untuk exclude
    INR_PATTERNS = [
        r'₹',               # Rupee symbol
        r'INR',             # INR
        r'Rs\.?\s?\d+',     # Rs. 100, Rs 100
        r'rupee',           # rupee
        r' rupees?\b',      # rupee, rupees
    ]

    def __init__(self, target_region: str = "US"):
        """
        Inisialisasi GeoValidator.

        Args:
            target_region: Region target (default: US).
        """
        self.target_region = target_region.upper()
        logger.info(f"GeoValidator diinisialisasi untuk region: {self.target_region}")

    def validate_tier1(
        self,
        title: str,
        description: str,
        channel_location: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Validasi Tier 1 audience dengan multi-factor scoring.

        Args:
            title: Video title.
            description: Video description.
            channel_location: Channel location dari YouTube API.

        Returns:
            Dict dengan validation results dan score.
        """
        # Combine text untuk analysis
        text = f"{title} {description}".lower()

        # Initialize scores
        scores = {
            "language": 0.0,      # Max 0.40
            "currency": 0.0,      # Max 0.30
            "cultural": 0.0,      # Max 0.20
            "region": 0.0,        # Max 0.10
        }

        # 1. Language Detection (40%)
        scores["language"] = self._detect_language(title, description)

        # 2. Currency Detection (30%)
        scores["currency"] = self._detect_currency(text)

        # 3. Cultural Context (20%)
        scores["cultural"] = self._detect_cultural_context(text)

        # 4. Region Check (10%)
        scores["region"] = self._check_region(channel_location)

        # Calculate total score
        total_score = sum(scores.values())

        # Determine pass/fail
        passed = total_score >= 0.70

        # Additional check: explicit exclude patterns
        has_exclude = self._has_exclude_patterns(text)

        if has_exclude:
            passed = False
            logger.debug(f"Tier1 FAILED: Exclude patterns detected")

        result = {
            "passed": passed and not has_exclude,
            "score": total_score,
            "scores": scores,
            "has_exclude_patterns": has_exclude,
            "target_region": self.target_region
        }

        logger.info(f"Tier1 validation: score={total_score:.2f}, passed={passed}")

        return result

    def _detect_language(self, title: str, description: str) -> float:
        """
        Detect language - English = 40%.

        Args:
            title: Video title.
            description: Video description.

        Returns:
            Score 0.0 - 0.40
        """
        if detect is None:
            # Fallback: simple keyword check
            text = f"{title} {description}".lower()
            us_keywords = sum(1 for kw in self.US_CULTURAL_KEYWORDS if kw in text)
            return min(0.40, us_keywords * 0.05)

        try:
            # Detect from title + description
            text = f"{title} {description}"
            lang = detect(text)

            if lang == "en":
                return 0.40  # Full score for English
            else:
                return 0.0

        except LangDetectException:
            # Short text or undetectable
            return 0.0

    def _detect_currency(self, text: str) -> float:
        """
        Detect USD currency presence = 30%.

        Args:
            text: Combined text.

        Returns:
            Score 0.0 - 0.30
        """
        score = 0.0

        # Check for USD patterns
        for pattern in self.USD_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                score += 0.10

        # Cap at 0.30
        score = min(0.30, score)

        # Penalty for INR patterns
        for pattern in self.INR_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                score = 0.0  # Zero score if INR detected
                break

        return score

    def _detect_cultural_context(self, text: str) -> float:
        """
        Detect US/Western cultural context = 20%.

        Args:
            text: Combined text.

        Returns:
            Score 0.0 - 0.20
        """
        score = 0.0

        # Check for US cultural keywords
        for keyword in self.US_CULTURAL_KEYWORDS:
            if keyword in text:
                score += 0.05

        # Cap at 0.20
        score = min(0.20, score)

        return score

    def _check_region(self, channel_location: Optional[str]) -> float:
        """
        Check if channel location = US = 10%.

        Args:
            channel_location: Channel location dari API.

        Returns:
            Score 0.0 - 0.10
        """
        if not channel_location:
            return 0.0  # No data = no score

        location_upper = channel_location.upper()

        # Check for US
        if "US" in location_upper or "USA" in location_upper or "UNITED STATES" in location_upper:
            return 0.10

        # Penalty for known non-US
        non_us = ["IN", "INDIA", "PK", "PAKISTAN", "BD", "BANGLADESH"]
        if any(country in location_upper for country in non_us):
            return 0.0

        return 0.0

    def _has_exclude_patterns(self, text: str) -> bool:
        """
        Check for explicit exclude patterns (non-US content).

        Args:
            text: Combined text.

        Returns:
            True jika exclude pattern detected.
        """
        for pattern in self.EXCLUDE_REGIONS:
            if pattern in text:
                return True

        return False


# Singleton instance
_validator_instance = None


def get_validator() -> GeoValidator:
    """Get or create GeoValidator singleton instance."""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = GeoValidator(target_region="US")
    return _validator_instance
