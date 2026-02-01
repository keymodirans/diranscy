# 11 SECURITY PERFORMANCE

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

---

## 14. SECURITY \& PERFORMANCE

### Security Best Practices

**1. API Key Protection**

```python
# ALWAYS: Load from environment variables or encrypted config
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# NEVER: Hardcode in source
# YOUTUBE_API_KEY = "AIzaSyABC123..."  # WRONG!
```

**2. SQL Injection Prevention**

```python
# ALWAYS: Use parameterized queries
cursor.execute("""
    SELECT * FROM videos WHERE video_id = ?
""", (video_id,))

# NEVER: String concatenation
# cursor.execute(f"SELECT * FROM videos WHERE video_id = '{video_id}'")  # WRONG!
```

**3. Input Sanitization**

```python
import html

def sanitize_for_prompt(user_input: str) -> str:
    """
    Sanitize user input before sending to Gemini AI.
    
    Prevents prompt injection attacks.
    """
    # HTML escape special characters
    safe_input = html.escape(user_input)
    
    # Remove control characters
    safe_input = ''.join(char for char in safe_input if ord(char) >= 32)
    
    return safe_input

# Usage
user_category = "History"
safe_category = sanitize_for_prompt(user_category)
prompt = f"Analyze category: {safe_category}"
```


---

### Performance Optimization

**1. Database Indexing**

```sql
-- Indexes already created in schema (Section 6)
CREATE INDEX idx_video_id ON videos(video_id);
CREATE INDEX idx_state ON videos(state);
CREATE INDEX idx_composite_score ON videos(composite_score DESC);
CREATE INDEX idx_tier1_validated ON videos(tier1_validated);
```

**2. Batch Processing (YouTube API)**

```python
# Process 50 video IDs per request (save quota)
def batch_process_videos(video_ids: list, batch_size: int = 50):
    """
    Process videos in batches.
    
    YouTube videos.list accepts up to 50 IDs per request.
    Cost: 1 unit (regardless of number of IDs)
    
    Savings: 50 IDs in 1 request (1 unit) vs 50 requests (50 units)
    """
    for i in range(0, len(video_ids), batch_size):
        batch = video_ids[i:i+batch_size]
        videos = youtube_videos_details(api_key, batch)
        yield videos
```

**3. Caching (Channel Subscriber Counts)**

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def get_channel_subscribers_cached(channel_id: str) -> int:
    """
    Cache channel subscriber counts (rarely change).
    
    Benefit: Avoid redundant API calls for same channel
    """
    return youtube_channel_subscribers(api_key, channel_id)

# Usage: Automatically cached
subs1 = get_channel_subscribers_cached("UC1234")  # API call
subs2 = get_channel_subscribers_cached("UC1234")  # Cached (no API call)
```

**4. Parallel Processing (Optional, Use with Caution)**

```python
from concurrent.futures import ThreadPoolExecutor

def transcribe_videos_parallel(video_urls: list, max_workers: int = 3):
    """
    Transcribe multiple videos concurrently.
    
    CAUTION:
    - Only use if Deepgram API rate limits allow
    - Monitor quota usage closely
    - Reduce max_workers if hitting rate limits
    
    Benefit: 3x faster transcription (3 parallel vs sequential)
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(deepgram_transcribe, url, api_key) for url in video_urls]
        results = [f.result() for f in futures]
    
    return results
```


---

