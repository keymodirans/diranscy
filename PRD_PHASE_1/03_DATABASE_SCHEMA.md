# 03 DATABASE SCHEMA

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

---

## 6. DATABASE DESIGN

### Database File

**Path:** `hunterbot.db` (SQLite database in application directory)

**Access Pattern:** Single-writer, single-reader (desktop app, no concurrency issues)

**Backup Strategy:** Auto-backup before each new scraping session to `hunterbot_backup_{timestamp}.db`

### Complete Schema Definition

```sql
-- ═══════════════════════════════════════════════════════════════════
-- TABLE 1: videos (Main video data & processing state)
-- ═══════════════════════════════════════════════════════════════════

CREATE TABLE videos (
    -- Primary Key
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    video_id TEXT UNIQUE NOT NULL,
    
    -- YouTube Metadata
    title TEXT NOT NULL,
    description TEXT,
    channel_id TEXT NOT NULL,
    channel_title TEXT NOT NULL,
    subscriber_count INTEGER NOT NULL,
    upload_date TEXT NOT NULL,  -- ISO 8601 format: "2026-01-15T10:30:00Z"
    duration TEXT NOT NULL,  -- ISO 8601 duration: "PT15M30S"
    duration_seconds INTEGER NOT NULL,
    category_id INTEGER,
    
    -- Statistics
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,

    -- Tags (for SEO reference and analysis)
    tags TEXT,  -- JSON array string: '["tag1", "tag2", "tag3"]'

    -- Thumbnail
    thumbnail_url TEXT NOT NULL,
    thumbnail_width INTEGER,
    thumbnail_height INTEGER,
    thumbnail_quality TEXT,  -- "maxres" | "standard" | "high" | "medium" | "default"
    
    -- Transcript
    transcript_raw TEXT,  -- Raw output from Deepgram/yt-dlp
    transcript_cleaned TEXT,  -- Cleaned by Sanitizer module
    transcript_source TEXT,  -- "deepgram" | "ytdlp"
    
    -- Chapters (stored as JSON string)
    has_chapters BOOLEAN DEFAULT 0,
    chapters_json TEXT,  -- JSON string format: '[{"timestamp":"0:00","seconds":0,"title":"Intro"}]'
                         -- Python: json.dumps(list) on insert, json.loads(str) on retrieve
    
    -- ML Features (calculated by Analyst module)
    v_score REAL,  -- views / subscriber_count
    like_view_ratio REAL,  -- likes / views
    comment_view_ratio REAL,  -- comments / views
    engagement_rate REAL,  -- (likes + comments) / views
    viral_velocity REAL,  -- views / upload_age_days
    upload_age_days INTEGER,
    composite_score REAL,  -- Final ranking score (0.0-1.0)
    
    -- Tier 1 Validation (Geo-Validator module)
    tier1_validated BOOLEAN DEFAULT 0,
    tier1_confidence_score REAL,  -- 0-100 confidence percentage
    tier1_validation_reason TEXT,  -- Why passed/failed validation
    
    -- AI Generated Content (Architect module)
    title_options TEXT,  -- JSON string: '["Title 1", "Title 2", "Title 3"]'
    edsa_script TEXT,  -- Full EDSA script (2000-5000 words)
    seo_description TEXT,  -- JSON string: '{"description":"...", "keywords":["k1","k2"]}'
    thumbnail_prompt TEXT,  -- Text prompt for image generation
    
    -- Processing State
    state TEXT DEFAULT 'RAW',  -- "RAW" | "CLEANED" | "OUTLIER" | "READY" | "EXPORTED" | "FAILED"
    error_message TEXT,  -- Error details if state="FAILED"
    data_quality_score REAL,  -- 0-100 quality score from Sanitizer
    
    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),  -- ISO 8601: "2026-02-01T20:30:45Z"
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Indexes for performance
CREATE INDEX idx_video_id ON videos(video_id);
CREATE INDEX idx_state ON videos(state);
CREATE INDEX idx_composite_score ON videos(composite_score DESC);
CREATE INDEX idx_tier1_validated ON videos(tier1_validated);

-- Trigger to auto-update updated_at timestamp
CREATE TRIGGER update_videos_timestamp 
AFTER UPDATE ON videos
BEGIN
    UPDATE videos SET updated_at = datetime('now') WHERE id = NEW.id;
END;

-- ═══════════════════════════════════════════════════════════════════
-- TABLE 2: api_keys (API key management & quota tracking)
-- ═══════════════════════════════════════════════════════════════════

CREATE TABLE api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service TEXT NOT NULL,  -- "youtube" | "deepgram" | "gemini"
    api_key TEXT NOT NULL,
    account_email TEXT,  -- For Deepgram accounts (optional)
    
    -- Status & Quota
    status TEXT DEFAULT 'ACTIVE',  -- "ACTIVE" | "EXHAUSTED" | "INVALID" | "SUSPENDED"
    quota_used INTEGER DEFAULT 0,
    quota_limit INTEGER,  -- YouTube: 10000, Deepgram: credit-based, Gemini: request-based
    
    -- Usage Tracking
    last_used TEXT,  -- ISO 8601 timestamp
    error_count INTEGER DEFAULT 0,
    
    -- Timestamps
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    
    -- Constraints
    UNIQUE(service, api_key)
);

CREATE INDEX idx_service_status ON api_keys(service, status);

-- ═══════════════════════════════════════════════════════════════════
-- TABLE 3: quota_log (Historical quota usage tracking)
-- ═══════════════════════════════════════════════════════════════════

CREATE TABLE quota_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_key_id INTEGER NOT NULL,
    service TEXT NOT NULL,
    quota_consumed INTEGER NOT NULL,
    endpoint TEXT,  -- API endpoint called: "search.list", "videos.list", etc.
    timestamp TEXT DEFAULT (datetime('now')),
    
    FOREIGN KEY (api_key_id) REFERENCES api_keys(id)
);

CREATE INDEX idx_quota_timestamp ON quota_log(timestamp DESC);

-- ═══════════════════════════════════════════════════════════════════
-- TABLE 4: config (Application configuration)
-- ═══════════════════════════════════════════════════════════════════

CREATE TABLE config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key TEXT UNIQUE NOT NULL,
    value TEXT,
    description TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);

-- Default configuration values
INSERT INTO config (key, value, description) VALUES
('current_category', NULL, 'Currently analyzed category'),
('current_sub_niche', NULL, 'Currently selected sub-niche'),
('target_video_count', '1000', 'Target number of videos to scrape'),
('last_export_path', NULL, 'Last Excel export file path'),
('app_version', '2.0.0', 'Application version'),
('tier1_only', '1', 'Filter only Tier 1 audience videos (1=yes, 0=no)'),
('target_regions', 'US,GB,CA,AU,DE,FR', 'Comma-separated Tier 1 country codes');

-- ═══════════════════════════════════════════════════════════════════
-- TABLE 5: processing_log (Activity logging)
-- ═══════════════════════════════════════════════════════════════════

CREATE TABLE processing_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module TEXT NOT NULL,  -- "classifier" | "hunter" | "sanitizer" | "geo_validator" | "analyst" | "architect" | "exporter" | "guardian"
    level TEXT DEFAULT 'INFO',  -- "DEBUG" | "INFO" | "WARNING" | "ERROR" | "CRITICAL"
    message TEXT NOT NULL,
    video_id TEXT,  -- Optional: related video_id
    timestamp TEXT DEFAULT (datetime('now')),
    
    -- Additional context (JSON string)
    context TEXT  -- '{"api_key_id": 3, "quota_used": 100}'
);

CREATE INDEX idx_module ON processing_log(module);
CREATE INDEX idx_level ON processing_log(level);
CREATE INDEX idx_timestamp ON processing_log(timestamp DESC);
```


### Example Data (For Model Understanding)

**Example 1: Video Record (state='READY')**

```sql
INSERT INTO videos (
    video_id, title, description, channel_id, channel_title, subscriber_count,
    upload_date, duration, duration_seconds, views, likes, comments,
    tags, thumbnail_url, thumbnail_quality, transcript_cleaned, has_chapters, chapters_json,
    v_score, like_view_ratio, engagement_rate, tier1_validated, tier1_confidence_score,
    title_options, edsa_script, seo_description, state, data_quality_score
) VALUES (
    'dQw4w9WgXcQ',
    'The Secret Weapon That Changed WW2 Forever',
    'Discover the untold story of the technology that shocked Nazi generals...',
    'UC1234567890',
    'History Uncovered',
    15000,
    '2025-12-15T10:00:00Z',
    'PT12M30S',
    750,
    185000,
    4200,
    320,
    '["ww2", "secret weapon", "nazi germany", "history documentary", "world war 2", "military technology"]',
    'https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
    'maxres',
    'World War 2 changed everything in 1944. One invention terrified the Nazi high command...',
    1,
    '[{"timestamp":"0:00","seconds":0,"title":"Introduction"},{"timestamp":"2:30","seconds":150,"title":"The Invention"}]',
    12.33,  -- 185000 views / 15000 subs
    0.0227,  -- 4200 likes / 185000 views
    0.0244,  -- (4200 + 320) / 185000
    1,
    95.5,
    '["The Secret Weapon That Changed WW2 Forever","What They Never Told You About WW2","The Hidden Truth Behind Nazi Germany\'s Defeat"]',
    'In 1944, the war was at a turning point. But one decision would change everything...',
    '{"description":"Discover the classified technology that changed World War 2...","keywords":["ww2 secrets","secret weapons","history documentary"]}',
    'READY',
    92.0
);
```

**Example 2: API Key Record**

```sql
INSERT INTO api_keys (service, api_key, status, quota_used, quota_limit) VALUES
('youtube', 'AIzaSyABC123...', 'ACTIVE', 2340, 10000),
('deepgram', 'abc123def456...', 'ACTIVE', 8500, 12000),
('gemini', 'xyz789uvw012...', 'ACTIVE', 45, 60);
```


### Query Patterns (Common Operations)

**1. Fetch videos for ML filtering:**

```sql
SELECT * FROM videos 
WHERE state = 'CLEANED' 
  AND tier1_validated = 1 
ORDER BY views DESC;
```

**2. Get next available API key:**

```sql
SELECT id, api_key, quota_used, quota_limit 
FROM api_keys 
WHERE service = 'youtube' 
  AND status = 'ACTIVE' 
  AND quota_used < quota_limit * 0.95 
ORDER BY quota_used ASC 
LIMIT 1;
```

**3. Update video state after processing:**

```sql
UPDATE videos 
SET state = 'OUTLIER', 
    composite_score = 0.875,
    updated_at = datetime('now')
WHERE id = 123;
```

**4. Log API quota usage:**

```sql
INSERT INTO quota_log (api_key_id, service, quota_consumed, endpoint) 
VALUES (3, 'youtube', 100, 'search.list');

UPDATE api_keys 
SET quota_used = quota_used + 100 
WHERE id = 3;
```


---

