# 12 TESTING STRATEGY

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

---

## 15. TESTING STRATEGY

### Unit Tests (Core Functions)

**Test Hunter Module:**

```python
# tests/test_hunter.py

import unittest
from hunterbot.modules.hunter import HunterModule

class TestHunterModule(unittest.TestCase):
    def setUp(self):
        # Initialize with test config
        self.hunter = HunterModule(guardian=None, deepgram_client=None, config={})
    
    def test_youtube_search_returns_valid_ids(self):
        """Test YouTube search returns 11-character video IDs."""
        video_ids, next_page = youtube_search(api_key="TEST_KEY", query="test", max_results=10)
        
        self.assertIsInstance(video_ids, list)
        self.assertEqual(len(video_ids), 10)
        self.assertTrue(all(len(vid_id) == 11 for vid_id in video_ids))
    
    def test_thumbnail_extraction_fallback(self):
        """Test thumbnail extraction with fallback cascade."""
        thumbnails = {
            'high': {'url': 'https://example.com/high.jpg', 'width': 480, 'height': 360},
            'default': {'url': 'https://example.com/default.jpg', 'width': 120, 'height': 90}
        }
        
        result = extract_thumbnail(thumbnails)
        
        self.assertEqual(result['quality'], 'high')
        self.assertEqual(result['width'], 480)
```

**Test Sanitizer Module:**

```python
# tests/test_sanitizer.py

import unittest
from hunterbot.modules.sanitizer import SanitizerModule

class TestSanitizerModule(unittest.TestCase):
    def setUp(self):
        self.sanitizer = SanitizerModule(config={})
    
    def test_filler_word_removal(self):
        """Test filler words are removed."""
        raw = "Um, so like, this is uh a test transcript."
        cleaned = self.sanitizer._clean_transcript(raw)
        
        self.assertNotIn("um", cleaned.lower())
        self.assertNotIn("like", cleaned.lower())
        self.assertNotIn("uh", cleaned.lower())
    
    def test_timestamp_removal(self):
        """Test timestamps are removed."""
        raw = "[00:15] This is a test [0:30] with timestamps."
        cleaned = self.sanitizer._clean_transcript(raw)
        
        self.assertNotIn("[00:15]", cleaned)
        self.assertNotIn("[0:30]", cleaned)
    
    def test_quality_score_calculation(self):
        """Test quality score calculation."""
        video = {
            'video_id': 'test123',
            'title': 'Valid Title',
            'views': 100000,
            'subscriber_count': 5000,
            'transcript_cleaned': 'A' * 500,  # 500 chars
            'duration_seconds': 300,
            'thumbnail_quality': 'high'
        }
        
        is_valid, score, errors = self.sanitizer._validate_metadata(video, video['transcript_cleaned'])
        
        self.assertTrue(is_valid)
        self.assertGreaterEqual(score, 50)
        self.assertEqual(len(errors), 0)
```


---

### Integration Tests

**Test ML Pipeline:**

```python
# tests/test_ml_pipeline.py

import unittest
import pandas as pd
from hunterbot.modules.analyst import AnalystModule

class TestMLPipeline(unittest.TestCase):
    def setUp(self):
        self.analyst = AnalystModule(config={
            'ml': {
                'isolation_forest': {'contamination': 0.1, 'random_state': 42},
                'dbscan': {'eps': 0.5, 'min_samples': 3}
            }
        })
    
    def test_end_to_end_filtering(self):
        """Test full ML pipeline (Isolation Forest + DBSCAN)."""
        # Load test dataset
        videos_df = pd.read_csv('tests/fixtures/videos_sample.csv')
        
        top_10 = self.analyst.filter_outliers(videos_df)
        
        # Assertions
        self.assertEqual(len(top_10), 10)
        self.assertTrue(all(top_10['composite_score'] > 0))
        self.assertTrue(top_10['composite_score'].is_monotonic_decreasing)
```


---

### Test Coverage Targets

| Module | Target Coverage | Critical Functions |
| :-- | :-- | :-- |
| Hunter | 80% | `scrape_videos()`, `extract_metadata()`, `extract_transcript()` |
| Sanitizer | 90% | `_clean_transcript()`, `_validate_metadata()` |
| Analyst | 85% | `filter_outliers()`, `_engineer_features()` |
| Architect | 75% | `generate_content()` (Gemini calls hard to mock) |
| Exporter | 80% | `export_to_excel()`, sheet creation methods |
| Guardian | 90% | `get_api_key()`, `log_quota_usage()` |


---

