# 04 MODULE SPECS

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

---

## 8. MODULE SPECIFICATIONS

### Module Overview Table

**Model Instruction:** Read this summary first, then refer to detailed specs below.


| Module | File Path | Class Name | Primary Methods | Dependencies |
| :-- | :-- | :-- | :-- | :-- |
| Classifier | `hunterbot/modules/classifier.py` | `ClassifierModule` | `classify_sub_niches()` | Gemini AI, Guardian |
| Hunter | `hunterbot/modules/hunter.py` | `HunterModule` | `scrape_videos()`, `extract_metadata()`, `extract_transcript()` | YouTube API, Deepgram API, Guardian |
| Sanitizer | `hunterbot/modules/sanitizer.py` | `SanitizerModule` | `clean_transcripts()`, `validate_metadata()` | regex, validators |
| Geo-Validator | `hunterbot/modules/geo_validator.py` | `GeoValidatorModule` | `validate_tier1()` | langdetect |
| Analyst | `hunterbot/modules/analyst.py` | `AnalystModule` | `filter_outliers()`, `engineer_features()` | scikit-learn, pandas |
| Architect | `hunterbot/modules/architect.py` | `ArchitectModule` | `generate_content()` | Gemini AI, Guardian |
| Exporter | `hunterbot/modules/exporter.py` | `ExporterModule` | `export_to_excel()` | openpyxl |
| Guardian | `hunterbot/modules/guardian.py` | `GuardianModule` | `get_api_key()`, `log_quota()`, `rate_limit()` | Database |


---

### 8.1 MODULE 1: CLASSIFIER (Round 1)

**File:** `hunterbot/modules/classifier.py`

**Purpose:** Analyze 1000 cleaned transcripts from broad category, cluster into 5 specific sub-niches using Gemini AI.

**Input:**

- Category name (string, e.g., "Horror")
- 1000 cleaned transcripts (from Sanitizer, Round 1)

**Output:**

- 5 sub-niche suggestions with metadata

**Process Flow (Round 1):**

```
1. Receive category + 1000 cleaned videos from Round 1 Sanitizer
2. Extract transcripts from cleaned video records
3. Send 1000 transcripts to Gemini AI for clustering
4. Parse Gemini response (JSON)
5. Return 5 sub-niche suggestions to UI
6. User selects 1 sub-niche
7. Store selected sub-niche in config table for Round 2
```

**Implementation Skeleton:**

```python
# hunterbot/modules/classifier.py

from hunterbot.modules.guardian import GuardianModule
from hunterbot.utils.logger import log_info, log_error
import requests
from typing import List, Dict

class ClassifierModule:
    def __init__(self, guardian: GuardianModule, gemini_client, config: dict):
        self.guardian = guardian
        self.gemini = gemini_client
        self.config = config

    def classify_sub_niches(self, category: str, cleaned_videos: list) -> Dict:
        """
        Main method: Cluster 1000 transcripts into 5 sub-niches.

        Args:
            category: Broad category name (e.g., "Horror")
            cleaned_videos: List of 1000 video records with cleaned transcripts

        Returns:
            dict: {
                'category': str,
                'sub_niches': [
                    {'name': str, 'video_count': int, 'demand': str, 'examples': list},
                    ...
                ]
            }
        """
        log_info("classifier", f"Clustering {len(cleaned_videos)} transcripts for category: {category}")

        # Step 1: Extract transcripts from cleaned videos
        transcripts = [v.transcript_cleaned for v in cleaned_videos if v.transcript_cleaned]
        titles = [v.title for v in cleaned_videos]

        log_info("classifier", f"Extracted {len(transcripts)} valid transcripts")

        # Step 2: Gemini clustering (1000 transcripts + titles)
        result = self.gemini.classify_sub_niches_from_transcripts(
            category,
            transcripts[:1000],  # Send up to 1000 transcripts
            titles[:1000]
        )

        log_info("classifier", f"Found {len(result['sub_niches'])} sub-niches")

        return result
```

**Verification Checklist:**

AFTER GENERATION:

- [ ] Imports at top (absolute paths from hunterbot.*)
- [ ] All functions have type hints
- [ ] Gemini API calls wrapped in try/except
- [ ] Sample size validated (>= 50 titles minimum)
- [ ] JSON parsing errors handled gracefully

---

### 8.2 MODULE 2: HUNTER (Runs in Both Rounds)

**File:** `hunterbot/modules/hunter.py`

**Purpose:** Scrape 1000 videos from YouTube, extract metadata and transcripts.

**Input (Round 1):**
- Category keyword (string, e.g., "Horror")

**Input (Round 2):**
- Selected sub-niche keyword (string, e.g., "Haunted House Stories")

**Output:**
- 1000 video records in database (state='RAW')

**Note:** Hunter module runs TWICE per session with different search queries.

- Use Guardian module for API key rotation
- Apply rate limiting (2-3 second delays)
- Log all API calls to processing_log table
- Retry failed API calls 3x with exponential backoff

**ASK FIRST:**

- If user wants to change default target count (1000)
- If user wants to adjust date range filter

**NEVER:**

- Hardcode API keys in this module
- Skip video if transcript unavailable (use fallback)
- Proceed without validating API key status

**Implementation Skeleton:**

```python
# hunterbot/modules/hunter.py

from hunterbot.modules.guardian import GuardianModule
from hunterbot.database.models import Video
from hunterbot.utils.logger import log_info, log_warning, log_error
from hunterbot.utils.validators import validate_video_id
from tenacity import retry, stop_after_attempt, wait_exponential
import requests
from typing import List
import time

class HunterModule:
    def __init__(self, guardian: GuardianModule, deepgram_client, config: dict):
        self.guardian = guardian
        self.deepgram = deepgram_client
        self.config = config
    
    def scrape_videos(self, sub_niche: str, target_count: int = 1000) -> int:
        """
        Main scraping orchestration.
        
        Returns:
            Number of videos successfully scraped
        """
        log_info("hunter", f"Starting scrape: {sub_niche}, target: {target_count}")
        
        # Step 1: Search videos
        video_ids = self._search_videos(sub_niche, target_count)
        log_info("hunter", f"Found {len(video_ids)} video IDs")
        
        # Step 2: Filter by channel size
        filtered_ids = self._filter_by_channel_size(video_ids)
        log_info("hunter", f"After channel filter: {len(filtered_ids)} videos")
        
        # Step 3: Extract metadata + transcripts
        success_count = 0
        for idx, video_id in enumerate(filtered_ids, 1):
            try:
                metadata = self._extract_metadata(video_id)
                transcript = self._extract_transcript(f"https://www.youtube.com/watch?v={video_id}")
                
                # Save to database
                self._save_to_database(metadata, transcript)
                success_count += 1
                
                # Progress logging
                if idx % 50 == 0:
                    log_info("hunter", f"Progress: {idx}/{len(filtered_ids)} videos")
                
                # Rate limiting
                self.guardian.rate_limit('youtube', delay=2)
            
            except Exception as e:
                log_error("hunter", f"Failed to process {video_id}: {e}")
                continue
        
        log_info("hunter", f"Scraping complete: {success_count} videos saved")
        return success_count
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def _search_videos(self, query: str, count: int) -> List[str]:
        """
        YouTube search with pagination.
        
        Quota cost: 100 units per request * (count / 50) requests
        """
        # Implementation in Section 7.1
        pass
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def _extract_metadata(self, video_id: str) -> dict:
        """Extract metadata using YouTube videos.list API."""
        # Implementation in Section 7.1
        pass
    
    def _extract_transcript(self, video_url: str) -> str:
        """
        Extract transcript with Deepgram (primary) + yt-dlp (fallback).
        
        Try order:
        1. Deepgram API (best accuracy)
        2. yt-dlp auto-captions (fallback if Deepgram fails)
        """
        # Implementation in Section 7.2
        pass
    
    def _save_to_database(self, metadata: dict, transcript: str):
        """Insert video record with state='RAW'."""
        # Implementation uses database/models.py
        pass
```

**Verification Checklist:**

AFTER GENERATION:

- [ ] All external API calls use @retry decorator
- [ ] Guardian.get_api_key() called for each request batch
- [ ] Guardian.rate_limit() called between requests
- [ ] Transcript fallback logic implemented (Deepgram → yt-dlp)
- [ ] Database insert uses parameterized queries
- [ ] Progress logged every 50 videos
- [ ] Total quota usage logged to quota_log table

---

### 8.3 MODULE 3: SANITIZER

**File:** `hunterbot/modules/sanitizer.py`

**Purpose:** Clean transcripts (regex), validate metadata quality.

**Input:**

- Videos with state='RAW'

**Output:**

- Videos with state='CLEANED' (quality score >= 50)
- Videos with state='FAILED' (quality score < 50)

**ALWAYS:**

- Remove ALL filler words (um, uh, like, you know)
- Remove timestamps and sound notations
- Validate transcript length (minimum 100 characters)
- Calculate quality score (0-100)

**NEVER:**

- Modify original transcript (keep transcript_raw intact)
- Skip validation (always calculate quality score)
- Proceed with quality score < 50

**Implementation:**

```python
# hunterbot/modules/sanitizer.py

import re
from hunterbot.database.models import Video
from hunterbot.utils.logger import log_info
from typing import Tuple

class SanitizerModule:
    def __init__(self, config: dict):
        self.config = config
        self.filler_words = ['um', 'uh', 'like', 'you know', 'kind of', 'sort of', 'actually']
    
    def clean_transcripts(self, videos: list) -> dict:
        """
        Clean all RAW videos.
        
        Returns:
            dict: {
                'cleaned': int,  # Count of videos with state='CLEANED'
                'failed': int    # Count of videos with state='FAILED'
            }
        """
        cleaned_count = 0
        failed_count = 0
        
        for video in videos:
            # Clean transcript
            cleaned = self._clean_transcript(video.transcript_raw)
            
            # Validate quality
            is_valid, score, errors = self._validate_metadata(video, cleaned)
            
            if is_valid:
                video.transcript_cleaned = cleaned
                video.data_quality_score = score
                video.state = 'CLEANED'
                cleaned_count += 1
            else:
                video.state = 'FAILED'
                video.error_message = "; ".join(errors)
                video.data_quality_score = score
                failed_count += 1
            
            video.save()
        
        log_info("sanitizer", f"Cleaned: {cleaned_count}, Failed: {failed_count}")
        
        return {'cleaned': cleaned_count, 'failed': failed_count}
    
    def _clean_transcript(self, raw_transcript: str) -> str:
        """
        Clean transcript using regex operations.
        
        Operations:
        1. Remove timestamps
        2. Remove filler words
        3. Remove sound notations
        4. Normalize whitespace
        5. Fix punctuation spacing
        """
        if not raw_transcript:
            return ""
        
        text = raw_transcript
        
        # Remove timestamps (00:00, 0:00, [00:00])
        text = re.sub(r'\[?\d{1,2}:\d{2}:\d{2}\]?', '', text)
        text = re.sub(r'\[?\d{1,2}:\d{2}\]?', '', text)
        
        # Remove filler words
        for filler in self.filler_words:
            text = re.sub(rf'\b{filler}\b', '', text, flags=re.IGNORECASE)
        
        # Remove music/sound notations
        text = re.sub(r'\[.*?\]', '', text)  # [Music], [Applause]
        text = re.sub(r'\(.*?\)', '', text)  # (laughing), (coughing)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces -> single space
        text = text.strip()
        
        # Fix punctuation spacing
        text = re.sub(r'\s+([.,!?])', r'\1', text)  # Remove space before punctuation
        
        return text
    
    def _validate_metadata(self, video, cleaned_transcript: str) -> Tuple[bool, float, list]:
        """
        Validate metadata quality.
        
        Returns:
            Tuple: (is_valid: bool, quality_score: float, errors: list)
        
        Scoring rubric:
        - Transcript length: 30 points (>100 chars)
        - Views threshold: 20 points (>1000 views)
        - Duration check: 50 points (>60 seconds, exclude Shorts)
        - Thumbnail quality: 10 points (>= high quality)
        
        Pass threshold: 50 points
        """
        errors = []
        score = 100.0
        
        # Check transcript length
        if len(cleaned_transcript) < 100:
            errors.append("Transcript too short (<100 chars)")
            score -= 30
        
        # Check views
        if video.views < 1000:
            errors.append("Views below threshold (<1000)")
            score -= 20
        
        # Check duration (exclude Shorts)
        if video.duration_seconds < 60:
            errors.append("Video too short (<60s), likely Shorts")
            score -= 50
        
        # Check thumbnail quality
        if video.thumbnail_quality == 'default':
            errors.append("Thumbnail quality too low")
            score -= 10
        
        is_valid = score >= 50
        
        return is_valid, max(0, score), errors
```

**Example Input/Output:**

**Input (Raw Transcript):**

```
[00:15] Um, so like, [Music] this is, uh, a test transcript about, you know, World War 2.
```

**Output (Cleaned Transcript):**

```
this is a test transcript about World War 2.
```

**Verification Checklist:**

AFTER GENERATION:

- [ ] Filler words list complete (um, uh, like, you know, kind of, sort of)
- [ ] Regex patterns tested (no over-removal of valid content)
- [ ] Quality scoring formula documented
- [ ] Pass threshold justified (50 = minimum acceptable quality)
- [ ] Errors logged to error_message field
- [ ] Original transcript preserved in transcript_raw

---

### 8.4 MODULE 4: GEO-VALIDATOR (Tier 1 Filtering)

**File:** `hunterbot/modules/geo_validator.py`

**Purpose:** Ensure videos appeal to Tier 1 audience (highest CPM countries).

**Input:**

- Videos with state='CLEANED'

**Output:**

- Videos with tier1_validated=1 (passed validation)
- Videos with tier1_validated=0 (failed validation)

**Tier 1 Countries:**
US, UK, Canada, Australia, Germany, France, Netherlands, Switzerland, Nordic countries

**Validation Signals:**


| Signal | Weight | Detection Method |
| :-- | :-- | :-- |
| Language (English) | 40% | langdetect library |
| Currency mentions | 30% | Regex pattern matching |
| Cultural references | 20% | Keyword matching |
| Region code | 10% | Already filtered by YouTube API |

**Pass Threshold:** 70% confidence score

**Implementation:**

```python
# hunterbot/modules/geo_validator.py

from langdetect import detect, LangDetectException
from hunterbot.utils.logger import log_info
import re

class GeoValidatorModule:
    def __init__(self, config: dict):
        self.config = config
        self.tier1_currencies = ['$', 'USD', '£', 'GBP', '€', 'EUR', 'CAD', 'AUD', 'CHF', 'SEK', 'NOK']
        self.tier2_currencies = ['₹', 'INR', 'Rp', 'IDR', '₱', 'PHP', 'R$', 'BRL', '¥', 'CNY', 'JPY']
        self.western_keywords = [
            # US-specific
            'dollar', 'american', 'usa', 'united states', 'new york', 'california', 'washington dc',
            'nfl', 'nba', 'mlb', 'nhl', 'super bowl', 'thanksgiving', '4th of july', 'independence day',
            
            # UK-specific
            'pound', 'british', 'uk', 'united kingdom', 'london', 'brexit', 'premier league', 'parliament',
            
            # General Western
            'christmas', 'halloween', 'black friday', 'cyber monday', 'valentine\'s day',
            'amazon', 'walmart', 'target', 'costco', 'apple', 'google', 'microsoft', 'tesla',
            'netflix', 'disney', 'hbo', 'spotify', 'mcdonalds', 'starbucks', 'coca cola'
        ]
    
    def validate_videos(self, videos: list) -> dict:
        """
        Validate Tier 1 appeal for all cleaned videos.
        
        Returns:
            dict: {
                'tier1_count': int,  # Passed validation
                'tier2_count': int   # Failed validation
            }
        """
        tier1_count = 0
        tier2_count = 0
        
        for video in videos:
            is_tier1, confidence, reason = self.validate_tier1(video)
            
            video.tier1_validated = 1 if is_tier1 else 0
            video.tier1_confidence_score = confidence
            video.tier1_validation_reason = reason
            video.save()
            
            if is_tier1:
                tier1_count += 1
            else:
                tier2_count += 1
        
        log_info("geo_validator", f"Tier 1: {tier1_count}, Tier 2/3: {tier2_count}")
        
        return {'tier1_count': tier1_count, 'tier2_count': tier2_count}
    
    def validate_tier1(self, video) -> tuple:
        """
        Validate single video for Tier 1 appeal.
        
        Returns:
            Tuple: (is_tier1: bool, confidence_score: float, reason: str)
        """
        score = 100.0
        reasons = []
        
        # Signal 1: Language Detection (40 points)
        if not self._is_english(video.title):
            score -= 40
            reasons.append("Non-English title")
        
        if video.transcript_cleaned and not self._is_english(video.transcript_cleaned):
            score -= 40
            reasons.append("Non-English transcript")
        
        # Signal 2: Currency Mentions (30 points)
        currency_signal = self._detect_currency(video.transcript_cleaned or "")
        if currency_signal == 'tier2':
            score -= 30
            reasons.append("Tier 2 currency detected")
        elif currency_signal == 'none':
            score -= 10
            reasons.append("No currency context")
        
        # Signal 3: Cultural References (20 points)
        if not self._has_western_references(video.transcript_cleaned or ""):
            score -= 20
            reasons.append("No Tier 1 cultural references")
        
        is_tier1 = score >= 70
        reason = "; ".join(reasons) if reasons else "Tier 1 validated"
        
        return is_tier1, score, reason
    
    def _is_english(self, text: str) -> bool:
        """Detect if text is English."""
        if not text or len(text) < 10:
            return False
        
        try:
            return detect(text) == 'en'
        except LangDetectException:
            # Fallback: Check ASCII ratio
            ascii_chars = sum(1 for c in text if ord(c) < 128)
            return (ascii_chars / len(text)) > 0.9
    
    def _detect_currency(self, text: str) -> str:
        """
        Detect currency mentions.
        
        Returns:
            'tier1' | 'tier2' | 'none'
        """
        text_lower = text.lower()
        
        has_tier1 = any(curr.lower() in text_lower for curr in self.tier1_currencies)
        has_tier2 = any(curr.lower() in text_lower for curr in self.tier2_currencies)
        
        if has_tier1:
            return 'tier1'
        elif has_tier2:
            return 'tier2'
        else:
            return 'none'
    
    def _has_western_references(self, text: str) -> bool:
        """Detect Western cultural references."""
        text_lower = text.lower()
        matches = sum(1 for keyword in self.western_keywords if keyword in text_lower)
        
        return matches >= 2  # At least 2 Western references
```

**Verification Checklist:**

AFTER GENERATION:

- [ ] langdetect library imported correctly
- [ ] Fallback ASCII detection implemented (if langdetect fails)
- [ ] Currency lists complete (Tier 1 vs Tier 2)
- [ ] Western keywords list comprehensive
- [ ] Confidence scoring formula documented
- [ ] Pass threshold justified (70 = strong Tier 1 signal)
- [ ] Results logged to database fields

---

### 8.5 MODULE 5: ANALYST (ML Outlier Detection)

**File:** `hunterbot/modules/analyst.py`

**Purpose:** Filter videos using Machine Learning (Isolation Forest + DBSCAN).

**Input:**

- Videos with state='CLEANED' AND tier1_validated=1

**Output:**

- Top 10 videos with state='OUTLIER'

**ML Pipeline:**

```
CLEANED Videos (tier1_validated=1)
    ↓
STAGE 1: Feature Engineering
    ↓
STAGE 2: Hard Filtering (subscriber <30k, views >50k)
    ↓
STAGE 3: Isolation Forest (1000 → ~50 outliers)
    ↓
STAGE 4: DBSCAN Clustering (50 → ~10-15 true outliers)
    ↓
STAGE 5: Ranking & Top 10 Selection
```

**Implementation:**

```python
# hunterbot/modules/analyst.py

from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
from hunterbot.utils.logger import log_info
from datetime import datetime

class AnalystModule:
    def __init__(self, config: dict):
        self.config = config
        self.iso_forest = IsolationForest(
            contamination=config['ml']['isolation_forest']['contamination'],
            random_state=config['ml']['isolation_forest']['random_state'],
            n_estimators=100
        )
        self.dbscan = DBSCAN(
            eps=config['ml']['dbscan']['eps'],
            min_samples=config['ml']['dbscan']['min_samples']
        )
        self.scaler = StandardScaler()
    
    def filter_outliers(self, videos_df: pd.DataFrame) -> pd.DataFrame:
        """
        Main ML filtering pipeline.
        
        Args:
            videos_df: DataFrame with cleaned, tier1-validated videos
        
        Returns:
            DataFrame with top 10 outliers
        """
        log_info("analyst", f"Starting ML filtering: {len(videos_df)} videos")
        
        # STAGE 1: Feature Engineering
        videos_df = self._engineer_features(videos_df)
        log_info("analyst", "Feature engineering complete")
        
        # STAGE 2: Hard Filtering
        filtered_df = self._hard_filter(videos_df)
        log_info("analyst", f"After hard filter: {len(filtered_df)} videos")
        
        if len(filtered_df) < 100:
            log_warning("analyst", f"Low video count after filtering: {len(filtered_df)}")
        
        # STAGE 3: Isolation Forest
        outlier_candidates = self._isolation_forest_filter(filtered_df)
        log_info("analyst", f"Isolation Forest outliers: {len(outlier_candidates)}")
        
        # STAGE 4: DBSCAN Clustering
        true_outliers = self._dbscan_refinement(outlier_candidates)
        log_info("analyst", f"DBSCAN true outliers: {len(true_outliers)}")
        
        # STAGE 5: Ranking & Top 10 Selection
        top_10 = self._rank_and_select(true_outliers, top_n=10)
        log_info("analyst", f"Top 10 selected, highest V-Score: {top_10.iloc['v_score']:.2f}")
        
        return top_10
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate ML features from raw YouTube data.
        
        Features:
        - v_score = views / subscriber_count
        - like_view_ratio = likes / views
        - comment_view_ratio = comments / views
        - engagement_rate = (likes + comments) / views
        - upload_age_days = (today - upload_date).days
        - viral_velocity = views / upload_age_days
        """
        # V-Score (primary viral indicator)
        df['v_score'] = df['views'] / df['subscriber_count']
        
        # Engagement ratios
        df['like_view_ratio'] = df['likes'] / df['views']
        df['comment_view_ratio'] = df['comments'] / df['views']
        df['engagement_rate'] = (df['likes'] + df['comments']) / df['views']
        
        # Upload age
        df['upload_date'] = pd.to_datetime(df['upload_date'])
        today = pd.Timestamp.now()
        df['upload_age_days'] = (today - df['upload_date']).dt.days
        
        # Viral velocity (views per day)
        df['viral_velocity'] = df['views'] / df['upload_age_days']
        
        # Handle edge cases (division by zero, infinity)
        df = df.replace([float('inf'), -float('inf')], 0)
        df = df.fillna(0)
        
        return df
    
    def _hard_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Apply rule-based filters.

        Criteria:
        - subscriber_count <= 30,000 (small channels only)
        - views >= 50,000 (minimum viral threshold)
        - views <= subscriber_count * 50 (anti-paid promotion, max 50x ratio)
        - upload_age_days >= 7 (exclude brand new videos)
        - upload_age_days <= 21 (max 3 weeks, recent viral only)

        Rationale:
        - Views max 50x subscriber: Prevent false positives from paid promotion
          Example: 1K subs with 200K views = likely paid ads (200x ratio = invalid)
        - 21 days max: Focus on current trending viral content
        """
        filtered = df[
            (df['subscriber_count'] <= 30000) &
            (df['views'] >= 50000) &
            (df['views'] <= df['subscriber_count'] * 50) &
            (df['upload_age_days'] >= 7) &
            (df['upload_age_days'] <= 21)
        ]

        return filtered
    
    def _isolation_forest_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Stage 3: Isolation Forest outlier detection.
        
        Features used: v_score, views, upload_age_days
        Output: Videos with anomaly score = -1 (outliers)
        """
        features = df[['v_score', 'views', 'upload_age_days']].values
        predictions = self.iso_forest.fit_predict(features)
        
        # -1 = outlier, 1 = inlier
        outliers = df[predictions == -1].copy()
        
        return outliers
    
    def _dbscan_refinement(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Stage 4: DBSCAN clustering to find true outliers.
        
        Features used: like_view_ratio, comment_view_ratio, v_score
        Output: Noise points (cluster label = -1) = true outliers
        """
        features = df[['like_view_ratio', 'comment_view_ratio', 'v_score']].values
        features_scaled = self.scaler.fit_transform(features)
        
        clusters = self.dbscan.fit_predict(features_scaled)
        
        # -1 = noise (true outliers with unique patterns)
        true_outliers = df[clusters == -1].copy()
        
        return true_outliers
    
    def _rank_and_select(self, df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
        """
        Stage 5: Composite scoring and ranking.
        
        Composite score = weighted sum of normalized features:
        - 50% v_score (primary indicator)
        - 30% engagement_rate (quality indicator)
        - 20% viral_velocity (momentum indicator)
        """
        # Normalize features to 0-1 range
        df['v_score_norm'] = (df['v_score'] - df['v_score'].min()) / (df['v_score'].max() - df['v_score'].min())
        df['engagement_norm'] = (df['engagement_rate'] - df['engagement_rate'].min()) / (df['engagement_rate'].max() - df['engagement_rate'].min())
        df['velocity_norm'] = (df['viral_velocity'] - df['viral_velocity'].min()) / (df['viral_velocity'].max() - df['viral_velocity'].min())
        
        # Composite score
        df['composite_score'] = (
            0.5 * df['v_score_norm'] +
            0.3 * df['engagement_norm'] +
            0.2 * df['velocity_norm']
        )
        
        # Sort and select top N
        top_df = df.nlargest(top_n, 'composite_score')
        
        return top_df
```

**Verification Checklist:**

AFTER GENERATION:

- [ ] scikit-learn imports correct (IsolationForest, DBSCAN, StandardScaler)
- [ ] Feature engineering formulas documented
- [ ] Hard filter thresholds justified (30k subs, 50k views)
- [ ] Isolation Forest hyperparameters documented
- [ ] DBSCAN hyperparameters documented
- [ ] Composite scoring weights justified (50/30/20)
- [ ] Edge cases handled (division by zero, infinity, NaN)
- [ ] Logging at each stage

---

### 8.6 MODULE 6: ARCHITECT (AI Content Generation)

**File:** `hunterbot/modules/architect.py`

**Purpose:** Generate EDSA scripts, titles, SEO, thumbnail prompts using Gemini AI.

**Input:**

- 10 videos with state='OUTLIER'

**Output:**

- 10 videos with state='READY' (all AI content generated)

**Process (Per Video):**

```
1. Generate 3 titles (Prompt 1)
2. Generate EDSA script (Prompt 2) + Validate banned terms
3. Generate SEO description (Prompt 3)
4. Generate thumbnail prompt (Prompt 4)
5. If all succeed → state='READY'
6. If any fail after 3 retries → state='FAILED'
```

**Implementation:**

```python
# hunterbot/modules/architect.py

from hunterbot.modules.guardian import GuardianModule
from hunterbot.utils.logger import log_info, log_warning, log_error
import json

class ArchitectModule:
    def __init__(self, guardian: GuardianModule, gemini_client, config: dict):
        self.guardian = guardian
        self.gemini = gemini_client
        self.config = config
    
    def generate_content(self, videos: list) -> dict:
        """
        Generate AI content for all outlier videos.
        
        Returns:
            dict: {
                'ready': int,  # Successfully processed
                'failed': int  # Failed after retries
            }
        """
        ready_count = 0
        failed_count = 0
        
        for idx, video in enumerate(videos, 1):
            log_info("architect", f"Processing video {idx}/{len(videos)}: {video.video_id}")
            
            try:
                # Prompt 1: Titles
                titles = self.gemini.generate_titles(
                    video.title,
                    video.transcript_cleaned[:500]
                )
                video.title_options = json.dumps(titles)
                log_info("architect", f"Generated {len(titles)} titles")
                
                # Prompt 2: EDSA Script
                chapters = json.loads(video.chapters_json) if video.has_chapters else []
                script = self.gemini.generate_edsa_script(
                    video.title,
                    video.transcript_cleaned,
                    chapters,
                    video.duration_seconds
                )
                video.edsa_script = script
                log_info("architect", f"Generated EDSA script ({len(script)} chars)")
                
                # Prompt 3: SEO
                seo = self.gemini.generate_seo_description(
                    titles,  # Use first title
                    script[:1000]
                )
                video.seo_description = json.dumps(seo)
                log_info("architect", "Generated SEO description")
                
                # Prompt 4: Thumbnail
                thumbnail_prompt = self.gemini.generate_thumbnail_prompt(
                    titles,
                    video.thumbnail_url
                )
                video.thumbnail_prompt = thumbnail_prompt
                log_info("architect", "Generated thumbnail prompt")
                
                # All prompts succeeded
                video.state = 'READY'
                video.save()
                ready_count += 1
                
                # Rate limiting
                self.guardian.rate_limit('gemini', delay=1)
            
            except Exception as e:
                log_error("architect", f"Failed to process {video.video_id}: {e}")
                video.state = 'FAILED'
                video.error_message = str(e)
                video.save()
                failed_count += 1
        
        log_info("architect", f"Content generation complete: {ready_count} ready, {failed_count} failed")
        
        return {'ready': ready_count, 'failed': failed_count}
```

**Verification Checklist:**

AFTER GENERATION:

- [ ] All Gemini API calls use @retry decorator (from gemini_client)
- [ ] Banned terms validation enforced (in gemini_client)
- [ ] JSON serialization for title_options, seo_description
- [ ] Chapters parsed from JSON string (json.loads)
- [ ] Rate limiting applied between videos
- [ ] Errors logged with video_id context
- [ ] State transitions documented (OUTLIER → READY/FAILED)

---

### 8.7 MODULE 7: EXPORTER

**File:** `hunterbot/modules/exporter.py`

**Purpose:** Export 10 production-ready content packages to Excel.

**Input:**

- 10 videos with state='READY'

**Output:**

- Excel file (.xlsx) with 3 sheets

**Implementation:**

```python
# hunterbot/modules/exporter.py

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import json
from datetime import datetime
from hunterbot.utils.logger import log_info

class ExporterModule:
    def __init__(self, config: dict):
        self.config = config
    
    def export_to_excel(self, videos_df, sub_niche: str) -> str:
        """
        Export videos to Excel with 3 sheets.
        
        Args:
            videos_df: DataFrame with 10 ready videos
            sub_niche: Sub-niche name for filename
        
        Returns:
            Filepath of exported Excel file
        """
        wb = Workbook()
        
        # Sheet 1: Summary
        ws_summary = wb.active
        ws_summary.title = "Summary"
        self._create_summary_sheet(ws_summary, videos_df)
        
        # Sheet 2: Generated Content
        ws_content = wb.create_sheet("Generated Content")
        self._create_content_sheet(ws_content, videos_df)
        
        # Sheet 3: Competitor Data
        ws_competitor = wb.create_sheet("Competitor Data")
        self._create_competitor_sheet(ws_competitor, videos_df)
        
        # Save file
        timestamp = datetime.now().strftime("%Y-%m-%d")
        safe_niche = sub_niche.replace(' ', '_').replace('/', '-')
        filename = f"Hunterbot_{safe_niche}_{timestamp}.xlsx"
        filepath = f"exports/{filename}"
        
        wb.save(filepath)
        log_info("exporter", f"Exported to: {filepath}")
        
        return filepath
    
    def _create_summary_sheet(self, ws, df):
        """Create Summary sheet with key metrics."""
        # Headers
        headers = [
            'Rank', 'Video ID', 'Original Title', 'Views', 'V-Score',
            'Composite Score', 'Upload Date', 'Duration', 'Channel Name',
            'Subscriber Count', 'Thumbnail URL'
        ]
        
        # Style headers
        header_fill = PatternFill(start_color="32A852", end_color="32A852", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')
        
        # Data rows
        for idx, row in df.iterrows():
            ws.append([
                idx + 1,  # Rank
                row['video_id'],
                row['title'],
                row['views'],
                round(row['v_score'], 2),
                round(row['composite_score'], 4),
                row['upload_date'],
                self._seconds_to_duration(row['duration_seconds']),
                row['channel_title'],
                row['subscriber_count'],
                row['thumbnail_url']
            ])
        
        # Auto-adjust column widths
        for col in ws.columns:
            max_length = 0
            col_letter = get_column_letter(col.column)
            for cell in col:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            ws.column_dimensions[col_letter].width = min(max_length + 2, 50)
    
    def _create_content_sheet(self, ws, df):
        """Create Generated Content sheet."""
        headers = [
            'Rank', 'Title Option 1', 'Title Option 2', 'Title Option 3',
            'EDSA Script', 'SEO Description', 'SEO Keywords', 'Thumbnail Prompt'
        ]
        
        # Headers with styling
        header_fill = PatternFill(start_color="3498DB", end_color="3498DB", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.fill = header_fill
            cell.font = header_font
        
        # Data rows
        for idx, row in df.iterrows():
            title_options = json.loads(row['title_options'])
            seo_data = json.loads(row['seo_description'])
            
            ws.append([
                idx + 1,
                title_options,
                title_options,[^1]
                title_options,[^2]
                row['edsa_script'],
                seo_data['description'],
                ', '.join(seo_data['keywords']),
                row['thumbnail_prompt']
            ])
            
            # Enable text wrapping for long content
            row_num = ws.max_row
            for col_num in:  # EDSA Script, SEO Desc, Thumbnail Prompt[^3][^4][^5]
                ws.cell(row=row_num, column=col_num).alignment = Alignment(wrap_text=True)
        
        # Set column widths
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 40
        ws.column_dimensions['C'].width = 40
        ws.column_dimensions['D'].width = 40
        ws.column_dimensions['E'].width = 80
        ws.column_dimensions['F'].width = 50
        ws.column_dimensions['G'].width = 50
        ws.column_dimensions['H'].width = 60
    
    def _create_competitor_sheet(self, ws, df):
        """Create Competitor Data sheet."""
        headers = [
            'Rank', 'Original Transcript', 'Chapters', 'Likes', 'Comments',
            'Like/View Ratio', 'Comment/View Ratio', 'Engagement Rate'
        ]
        
        header_fill = PatternFill(start_color="E74C3C", end_color="E74C3C", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")
        
        for col_num, header in enumerate(headers, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.value = header
            cell.fill = header_fill
            cell.font = header_font
        
        for idx, row in df.iterrows():
            ws.append([
                idx + 1,
                row['transcript_cleaned'],
                row['chapters_json'],
                row['likes'],
                row['comments'],
                round(row['like_view_ratio'], 6),
                round(row['comment_view_ratio'], 6),
                round(row['engagement_rate'], 6)
            ])
            
            row_num = ws.max_row
            ws.cell(row=row_num, column=2).alignment = Alignment(wrap_text=True)
        
        ws.column_dimensions['A'].width = 8
        ws.column_dimensions['B'].width = 100
        ws.column_dimensions['C'].width = 50
    
    def _seconds_to_duration(self, seconds: int) -> str:
        """Convert seconds to MM:SS or HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
```

**Verification Checklist:**

AFTER GENERATION:

- [ ] openpyxl imported correctly
- [ ] 3 sheets created with distinct purposes
- [ ] Headers styled (color fill, bold font)
- [ ] JSON parsing for title_options, seo_description, chapters_json
- [ ] Text wrapping enabled for long content columns
- [ ] Column widths set appropriately
- [ ] Filename sanitized (spaces → underscores, special chars removed)
- [ ] Export path logged

---

### 8.8 MODULE 8: GUARDIAN (API Key Rotation \& Rate Limiting)

**File:** `hunterbot/modules/guardian.py`

**Purpose:** Manage API key rotation, quota tracking, rate limiting.

**Responsibilities:**

1. API key rotation (round-robin)
2. Quota monitoring
3. Rate limiting (delays between requests)
4. Error detection (quota exceeded, invalid key)

**Implementation:**

```python
# hunterbot/modules/guardian.py

import time
from datetime import datetime
import sqlite3
from hunterbot.utils.logger import log_info, log_warning, log_error

class GuardianModule:
    def __init__(self, db_path: str, config: dict):
        self.db_path = db_path
        self.config = config
        self.current_youtube_key_index = 0
        self.current_deepgram_account_index = 0
        self.current_gemini_key_index = 0
    
    def get_api_key(self, service: str) -> tuple:
        """
        Get next available API key (round-robin).
        
        Args:
            service: 'youtube' | 'deepgram' | 'gemini'
        
        Returns:
            Tuple: (api_key: str, key_id: int)
        
        Raises:
            Exception: If no active keys available
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get all active keys for service
        cursor.execute("""
            SELECT id, api_key, quota_used, quota_limit
            FROM api_keys
            WHERE service = ? AND status = 'ACTIVE'
            ORDER BY id
        """, (service,))
        
        keys = cursor.fetchall()
        
        if not keys:
            conn.close()
            raise Exception(f"No active {service} API keys available")
        
        # Round-robin selection
        if service == 'youtube':
            index = self.current_youtube_key_index % len(keys)
            self.current_youtube_key_index += 1
        elif service == 'deepgram':
            index = self.current_deepgram_account_index % len(keys)
            self.current_deepgram_account_index += 1
        elif service == 'gemini':
            index = self.current_gemini_key_index % len(keys)
            self.current_gemini_key_index += 1
        else:
            index = 0
        
        key_id, api_key, quota_used, quota_limit = keys[index]
        
        # Check quota (warn at 95%)
        if quota_limit and quota_used >= quota_limit * 0.95:
            log_warning("guardian", f"{service} key #{key_id} quota 95% full, rotating...")
            # Recursive call to get next key
            conn.close()
            return self.get_api_key(service)
        
        # Update last_used timestamp
        cursor.execute("""
            UPDATE api_keys
            SET last_used = ?
            WHERE id = ?
        """, (datetime.now().isoformat(), key_id))
        
        conn.commit()
        conn.close()
        
        return api_key, key_id
    
    def log_quota_usage(self, key_id: int, service: str, quota_consumed: int, endpoint: str = None):
        """Log API quota consumption."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Update api_keys table
        cursor.execute("""
            UPDATE api_keys
            SET quota_used = quota_used + ?
            WHERE id = ?
        """, (quota_consumed, key_id))
        
        # Insert into quota_log
        cursor.execute("""
            INSERT INTO quota_log (api_key_id, service, quota_consumed, endpoint)
            VALUES (?, ?, ?, ?)
        """, (key_id, service, quota_consumed, endpoint))
        
        conn.commit()
        conn.close()
    
    def mark_key_invalid(self, key_id: int, error_message: str):
        """Mark API key as invalid after errors."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE api_keys
            SET status = 'INVALID', error_count = error_count + 1
            WHERE id = ?
        """, (key_id,))
        
        conn.commit()
        conn.close()
        
        log_error("guardian", f"API key #{key_id} marked as INVALID: {error_message}")
    
    def rate_limit(self, service: str, delay: float = None):
        """
        Apply rate limiting delay.
        
        Args:
            service: 'youtube' | 'deepgram' | 'gemini'
            delay: Custom delay in seconds (optional)
        """
        if delay is None:
            delays = {
                'youtube': 2,
                'deepgram': 2,
                'gemini': 1
            }
            delay = delays.get(service, 2)
        
        time.sleep(delay)
```

**Verification Checklist:**

AFTER GENERATION:

- [ ] Round-robin rotation implemented correctly
- [ ] Quota threshold check (95%) before returning key
- [ ] Recursive call for next key if quota exceeded
- [ ] Quota logging to both api_keys and quota_log tables
- [ ] Timestamp updates use ISO 8601 format
- [ ] Rate limiting delays configurable
- [ ] Error handling for no active keys scenario

---

