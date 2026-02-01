<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Oke generate sekarang yang rapih. no emoji no icon menganggu clean PRD.

```markdown
# HUNTERBOT - PRODUCT REQUIREMENTS DOCUMENT (PRD)

**Version:** 2.0  
**Last Updated:** February 1, 2026  
**Document Status:** Production-Ready  
**Author:** The Sentinel Architect  
**Project Type:** Desktop Application (Windows)

---

## DOCUMENT CONTROL

### Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-02-01 | Initial draft | The Sentinel Architect |
| 2.0 | 2026-02-01 | Critical fixes, Tier 1 filtering, Best practices integration | The Sentinel Architect |

### Changelog (v2.0)

**CRITICAL FIXES:**
1. Fixed tech stack inconsistencies (explicit openpyxl, yt-dlp + ffmpeg dependency)
2. Completed code snippets (removed placeholders)
3. Added specific retry logic with decorator examples
4. Defined state transition rollback strategy
5. Clarified database schema JSON storage format
6. Added complete file structure with import paths
7. Provided complete Lucide icons list (8 icons, exact filenames, sizes)
8. Corrected Nuitka build config syntax
9. Added prompt injection protection (HTML escape)
10. Defined logging strategy (levels, rotation, export)
11. Added Module 8: Geo-Validator (Tier 1 filtering)
12. Updated database schema with tier1 validation fields

**v2.1 UPDATES (User Corrections):**
13. Added tags field to database schema (JSON array for SEO/analysis)
14. Updated hard filter: upload_age_days max changed from 365 to 21 (3 weeks)
15. Updated hard filter: added views <= subscriber_count × 50 (anti-paid promotion)
16. Updated YouTube API integration to include tags in metadata extraction
17. Updated examples with tags field included

**v2.1.1 UPDATES (2-Round Architecture):**
18. Changed from 1-round to 2-round scraping architecture
19. Round 1: Exploratory scraping (1000 videos) → Clustering → 5 sub-niches
20. Round 2: Focused scraping (1000 NEW videos) → ML filtering → Content generation
21. Updated Classifier module to use 1000 transcripts instead of 100 titles
22. Updated Hunter module to run twice (category → sub-niche)
23. Added GeminiClient.classify_sub_niches_from_transcripts() method
24. Updated total videos processed: 1000 → 2000 per session
25. Updated processing time: 50-70 min → 100-140 min
26. Updated UI workflow from 7 steps to 11 steps (2 rounds)

**ENHANCEMENTS:**
- Model-optimized structure (hierarchical, progressive disclosure)
- Explicit Always/Ask/Never boundaries
- Example-driven specifications
- Complete dependency matrix
- Self-verification checklists
- Import path specifications

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Product Vision & Goals](#2-product-vision--goals)
3. [Target Users](#3-target-users)
4. [System Architecture](#4-system-architecture)
5. [Tech Stack & Dependencies](#5-tech-stack--dependencies)
6. [Database Design](#6-database-design)
7. [API Integration](#7-api-integration)
8. [Module Specifications](#8-module-specifications)
9. [Machine Learning Pipeline](#9-machine-learning-pipeline)
10. [User Interface Design](#10-user-interface-design)
11. [Data Flow & State Management](#11-data-flow--state-management)
12. [Error Handling & Recovery](#12-error-handling--recovery)
13. [Logging Strategy](#13-logging-strategy)
14. [Security & Performance](#14-security--performance)
15. [Testing Strategy](#15-testing-strategy)
16. [Deployment Guide](#16-deployment-guide)
17. [Code Generation Instructions](#17-code-generation-instructions)
18. [Appendix: Decision Log](#18-appendix-decision-log)

---

## 1. EXECUTIVE SUMMARY

### Product Overview

**Hunterbot** is a Windows desktop application that automates YouTube viral video discovery and EDSA script generation for faceless content creators. The system uses a 2-round architecture: Round 1 explores broad categories to find sub-niches, Round 2 analyzes 1000 videos in the selected sub-niche to identify 10 true viral outliers using Machine Learning (Isolation Forest + DBSCAN), and generates production-ready content packages using Gemini AI.

**Core Workflow (2-Round Architecture):**

**ROUND 1: EXPLORATORY (Sub-Niche Discovery)**
1. User inputs broad category (e.g., "Horror")
2. Bot scrapes 1000 video metadata + transcripts (exploratory search)
3. Data cleaning (Sanitizer)
4. Gemini AI clusters 1000 cleaned transcripts → 5 sub-niche suggestions
5. User selects 1 sub-niche (e.g., "Haunted House Stories")

**ROUND 2: FOCUSED (Content Generation)**
6. Bot scraps 1000 NEW videos focused on selected sub-niche
7. Data cleaning (Sanitizer)
8. Geo-Validator filters Tier 1 audience only
9. ML filters to 10 true outliers (with strict quality gates)
10. Gemini AI generates EDSA scripts, titles, SEO, thumbnail prompts
11. Export to Excel with all production assets

**Quality Gates (Round 2 ML Pipeline):**
- Views: 50K - 50K-50×subscriber (anti-paid promotion)
- Upload age: 7-21 days (recent viral content only)
- Subscriber count: ≤ 30K (small channels with viral potential)

**Total Videos Processed:** 2000 videos per session (1000 exploratory + 1000 focused)

**Value Proposition:**
- Reduce content research time from 10+ hours to 60 minutes
- Data-driven viral video discovery (eliminate guesswork)
- AI-powered script generation (mimic winning patterns)
- Tier 1 geo-targeting (maximize CPM revenue)

**Success Metrics:**
- Process 2000 videos per session (1000 exploratory + 1000 focused) in under 120 minutes
- Achieve 90%+ outlier detection precision
- Generate 10 production-ready content packages per run
- Zero manual intervention required after initial setup

---

## 2. PRODUCT VISION & GOALS

### Primary Goal

Replicate Ryan Laks' faceless YouTube methodology with full automation:

1. **Find viral videos** in specific sub-niche with Tier 1 audience appeal
2. **Reverse engineer** content strategy (hook, structure, retention tactics)
3. **Generate original scripts** that mimic winning patterns without plagiarism
4. **Scale content production** from 1 video/week to 10 videos/week

### Secondary Goals

- **Democratize competitor research** - Enable non-technical users to analyze viral videos
- **Increase content quality** - Data-driven decisions vs creative guesswork
- **Maximize revenue** - Focus on Tier 1 audience (highest CPM countries)

### Non-Goals (Out of Scope)

- Video editing automation
- Voice-over generation (text-to-speech)
- Thumbnail design/generation (only generate prompts for external tools)
- YouTube upload automation
- Multi-platform support (Mac/Linux) - Windows only for v1.0
- Real-time monitoring/alerts

---

## 3. TARGET USERS

### Primary Persona: Faceless YouTube Creator

**Demographics:**
- Age: 25-45
- Background: Solopreneur, content creator, digital marketer
- Technical skill: Low to medium (can install software, setup API keys)
- Experience: 6+ months YouTube experience, familiar with faceless content

**Pain Points:**
1. **Manual research is time-consuming** - Spending 10+ hours per week finding viral topics
2. **Difficulty identifying organic virality** - Can't distinguish paid promotion vs organic growth
3. **Script quality inconsistent** - Struggle to replicate competitor's engagement patterns
4. **Low CPM from wrong audience** - Creating content that attracts Tier 2/3 viewers

**Goals:**
- Find proven viral topics in niche with high search volume
- Understand winning content structure and retention tactics
- Generate high-quality scripts quickly
- Maximize revenue per 1000 views (focus on Tier 1 countries)

**Use Case Workflow:**

```

Day 1:

- Launch Hunterbot
- Input category: "History"
- Review 5 AI-suggested sub-niches
- Select: "World War 2 Battles"
- Start scraping (run overnight)

Day 2:

- Review Excel export with 10 content packages
- Select top 3 scripts based on V-Score
- Produce videos (voice-over, editing)
- Upload to YouTube with generated titles/SEO

Week 1 Results:

- 3 videos published (from 10 options)
- 2/3 videos hit 50k+ views in 7 days
- Average CPM: \$15 (Tier 1 audience)
- Time saved: 25 hours of manual research

```

---

## 4. SYSTEM ARCHITECTURE

### High-Level Architecture Diagram

```

┌─────────────────────────────────────────────────────────────────────┐
│                         HUNTERBOT SYSTEM                             │
│                    (Single-User Desktop Application)                 │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  PRESENTATION LAYER                                                  │
│  CustomTkinter GUI (2-Round Workflow)                               │
│  ROUND 1 - EXPLORATORY:                                             │
│  - Step 1: Category Input                                           │
│  - Step 2: Scraping Progress (1000 videos)                          │
│  - Step 3: Cleaning Progress                                        │
│  - Step 4: Sub-Niche Suggestions (Gemini)                           │
│  - Step 5: Sub-Niche Selection                                      │
│  ROUND 2 - FOCUSED:                                                 │
│  - Step 6: Focused Scraping (1000 NEW videos)                       │
│  - Step 7: Cleaning + Geo-Filtering                                 │
│  - Step 8: ML Filtering Results                                     │
│  - Step 9: AI Script Generation Progress                            │
│  - Step 10: Export Results                                          │
│  - Step 11: Success Summary                                         │
└─────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│  CONTROLLER LAYER                                                    │
│  State Machine Orchestrator                                         │
│  - Manage state transitions (RAW → CLEANED → OUTLIER → READY)      │
│  - Coordinate module execution                                      │
│  - Handle errors and rollback logic                                 │
│  - Update UI with progress events                                   │
└─────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│  BUSINESS LOGIC LAYER (8 Core Modules)                              │
├─────────────────────────────────────────────────────────────────────┤
│  1. CLASSIFIER    → Auto sub-niche detection (Gemini AI)           │
│  2. HUNTER        → Scraping (YouTube API, Deepgram API)           │
│  3. SANITIZER     → Data cleaning (Regex, validation)              │
│  4. GEO-VALIDATOR → Tier 1 filtering (Language, currency signals)  │
│  5. ANALYST       → ML outlier detection (Isolation Forest+DBSCAN) │
│  6. ARCHITECT     → Content generation (Gemini AI, 4 prompts)      │
│  7. EXPORTER      → Excel export (openpyxl, 3 sheets)              │
│  8. GUARDIAN      → API key rotation \& rate limiting               │
└─────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│  DATA LAYER                                                          │
│  SQLite Database (hunterbot.db)                                     │
│  - videos (metadata, transcripts, ML features, AI outputs)          │
│  - api_keys (YouTube, Deepgram, Gemini key management)             │
│  - quota_log (API usage tracking)                                   │
│  - config (application settings)                                    │
│  - processing_log (activity logs)                                   │
└─────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────┐
│  EXTERNAL APIS                                                       │
│  - YouTube Data API v3 (metadata, channel data)                     │
│  - Deepgram API (audio transcription)                               │
│  - Gemini AI (sub-niche classification, script generation)          │
│  - yt-dlp (fallback transcript extraction, audio download)          │
└─────────────────────────────────────────────────────────────────────┘

```

### Module Summary Table

**Model Instruction:** Read this table first to understand system architecture, then dive into detailed module specs in Section 8.

**2-Round Architecture:**

| Module | Round | Purpose | Input | Output | External Dependencies | Processing Time |
|--------|-------|---------|-------|--------|----------------------|-----------------|
| **Hunter** | 1 | Exploratory scraping | Category (str) | 1000 video records (RAW) | YouTube API, Deepgram API | 30-40 minutes |
| **Sanitizer** | 1 | Clean transcripts | Videos (RAW) | Videos (CLEANED) | None | 2-3 minutes |
| **Classifier** | 1 | Sub-niche clustering | 1000 cleaned transcripts | 5 sub-niche suggestions | Gemini AI | 30-60 seconds |
| **Hunter** | 2 | Focused scraping | Selected sub-niche (str) | 1000 NEW video records (RAW) | YouTube API, Deepgram API | 30-40 minutes |
| **Sanitizer** | 2 | Clean transcripts | Videos (RAW) | Videos (CLEANED) | None | 2-3 minutes |
| **Geo-Validator** | 2 | Tier 1 filtering | Videos (CLEANED) | Videos (tier1_validated=1) | langdetect | 1-2 minutes |
| **Analyst** | 2 | ML outlier detection | Videos (tier1_validated=1) | Top 10 videos (OUTLIER) | scikit-learn | <1 minute |
| **Architect** | 2 | Content generation | Videos (OUTLIER) | Videos (READY) | Gemini AI | 15-20 minutes |
| **Exporter** | 2 | Create Excel | Videos (READY) | Excel file (.xlsx) | openpyxl | <30 seconds |
| **Guardian** | Both | API key rotation | N/A (background) | N/A | None | Continuous |

**Total Pipeline Duration:** 100-140 minutes (2000 videos total → 10 scripts)

**Hard Filter Criteria (Analyst Module - Round 2 only):**
- subscriber_count ≤ 30,000 (small channels only)
- views ≥ 50,000 AND views ≤ subscriber_count × 50 (anti-paid promotion)
- upload_age_days: 7-21 (recent viral only, max 3 weeks)

---

## 5. TECH STACK & DEPENDENCIES

### Core Technologies

| Component | Technology | Version | Justification |
|-----------|-----------|---------|---------------|
| **Language** | Python | 3.11+ | Type hints, performance improvements, mature ecosystem |
| **GUI Framework** | CustomTkinter | 5.2.0 | Modern dark-mode UI, active development, cross-platform |
| **Database** | SQLite | 3.40+ | Embedded database, zero configuration, ACID compliant |
| **ML Library** | scikit-learn | 1.4.0 | Production-ready ML algorithms, excellent documentation |
| **Data Processing** | pandas | 2.2.0 | Efficient DataFrame operations, ML integration |
| **Excel Export** | openpyxl | 3.1.2 | Write .xlsx files with formatting, charts support |
| **Image Processing** | Pillow | 10.2.0 | PNG icon loading for CustomTkinter |
| **Packaging** | Nuitka | 1.9.0 | Compile to native executable, better performance than PyInstaller |

### Complete Dependency Matrix

**requirements.txt (Direct Dependencies):**

```


# GUI Framework

customtkinter==5.2.0

# HTTP \& API Clients

requests==2.31.0
google-api-python-client==2.110.0
google-auth==2.25.0
google-auth-oauthlib==1.2.0
google-auth-httplib2==0.2.0
deepgram-sdk==3.2.0
google-generativeai==0.3.2

# Data Processing

pandas==2.2.0
numpy==1.26.0

# Machine Learning

scikit-learn==1.4.0

# Video Processing

yt-dlp==2024.01.01

# Excel Export

openpyxl==3.1.2

# Image Processing

Pillow==10.2.0

# Utilities

langdetect==1.0.9
tenacity==8.2.3
python-dotenv==1.0.0

# Development (Optional)

pytest==7.4.0
black==23.12.0

```

### System Dependencies (Must Install Manually)

**CRITICAL:** These are NOT Python packages and must be installed separately.

**1. ffmpeg (Required by yt-dlp for audio extraction)**

```bash
# Windows (using Chocolatey)
choco install ffmpeg

# Verify installation
ffmpeg -version
# Expected output: ffmpeg version 6.0 or higher
```

**Why needed:** yt-dlp uses ffmpeg to extract audio from YouTube videos for Deepgram transcription. Without ffmpeg, audio download will fail.

**2. Microsoft Visual C++ Redistributable (Required by some Python packages)**

```bash
# Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
# Install silently (for deployment)
vc_redist.x64.exe /install /quiet /norestart
```

**Why needed:** Some compiled Python packages (e.g., numpy, pandas) require MSVC runtime libraries.

### Installation Script (setup_dependencies.bat)

```batch
@echo off
echo Installing Hunterbot Dependencies...
echo.

echo [1/3] Installing Python packages...
pip install -r requirements.txt

echo.
echo [2/3] Checking ffmpeg installation...
where ffmpeg >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: ffmpeg not found!
    echo Please install ffmpeg: choco install ffmpeg
    exit /b 1
) else (
    echo ffmpeg found: OK
)

echo.
echo [3/3] Verifying installations...
python -c "import customtkinter; print('CustomTkinter:', customtkinter.__version__)"
python -c "import sklearn; print('scikit-learn:', sklearn.__version__)"
python -c "import deepgram; print('Deepgram SDK:', deepgram.__version__)"

echo.
echo Installation complete!
pause
```


### Import Conventions

**ALWAYS use absolute imports from project root:**

```python
# CORRECT (absolute imports)
from hunterbot.database.models import Video
from hunterbot.modules.hunter import HunterModule
from hunterbot.utils.validators import validate_metadata

# INCORRECT (relative imports - error-prone)
from .models import Video
from ..utils.validators import validate_metadata
```

**Why:** Absolute imports prevent circular dependency issues and make refactoring safer.

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

## 7. API INTEGRATION

### 7.1 YouTube Data API v3

**Official Documentation:** https://developers.google.com/youtube/v3/docs

**Authentication:**

- Method: API Key (query parameter `key`)
- Obtain key: Google Cloud Console > APIs \& Services > Credentials
- Quota: 10,000 units per day per project
- Quota reset: Daily at midnight Pacific Time

**Quota Costs:**


| Operation | Endpoint | Cost (units) |
| :-- | :-- | :-- |
| Search videos | `search.list` | 100 |
| Get video details | `videos.list` | 1 |
| Get channel details | `channels.list` | 1 |

**Strategy:** Use 5 API keys = 50,000 units/day capacity (enough for 5 full runs)

#### Endpoint 1: search.list (Video Discovery)

**Purpose:** Search YouTube videos by keyword, filter by region and language.

**Implementation:**

```python
import requests
from typing import List, Tuple, Optional

def youtube_search(
    api_key: str,
    query: str,
    max_results: int = 50,
    published_after: Optional[str] = None,
    region_code: str = 'US',
    page_token: Optional[str] = None
) -> Tuple[List[str], Optional[str]]:
    """
    Search YouTube videos with Tier 1 geo-targeting.
    
    Args:
        api_key: YouTube Data API key
        query: Search keyword (sub-niche name)
        max_results: Results per page (max 50)
        published_after: ISO 8601 date (e.g., "2025-01-01T00:00:00Z")
        region_code: Target country code ("US" for Tier 1)
        page_token: Pagination token from previous response
    
    Returns:
        Tuple of (video_ids: list, next_page_token: str or None)
    
    Raises:
        QuotaExceededException: If API quota exhausted
        InvalidAPIKeyException: If API key is invalid
    """
    url = 'https://www.googleapis.com/youtube/v3/search'
    
    params = {
        'key': api_key,
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'order': 'viewCount',  # Sort by views (descending)
        'maxResults': max_results,
        'regionCode': region_code,  # Tier 1 targeting
        'relevanceLanguage': 'en',  # English content only
        'videoDefinition': 'any',  # Include all quality levels
        'videoEmbeddable': 'true',  # Only embeddable videos
    }
    
    if published_after:
        params['publishedAfter'] = published_after
    
    if page_token:
        params['pageToken'] = page_token
    
    response = requests.get(url, params=params, timeout=30)
    
    # Error handling
    if response.status_code != 200:
        handle_youtube_api_error(response)
    
    data = response.json()
    
    # Extract video IDs
    video_ids = [item['id']['videoId'] for item in data.get('items', [])]
    next_page_token = data.get('nextPageToken')
    
    return video_ids, next_page_token


def handle_youtube_api_error(response: requests.Response):
    """Handle YouTube API errors with specific exceptions."""
    if response.status_code == 403:
        error_data = response.json()
        error_reason = error_data['error']['errors']['reason']
        
        if error_reason == 'quotaExceeded':
            raise QuotaExceededException("YouTube API quota exceeded for this key")
        elif error_reason == 'forbidden':
            raise InvalidAPIKeyException("YouTube API key is invalid or restricted")
    
    elif response.status_code == 404:
        raise VideoNotFoundException("Requested video not found")
    
    elif response.status_code >= 500:
        raise YouTubeServerException(f"YouTube API server error: {response.status_code}")
    
    else:
        raise Exception(f"YouTube API error {response.status_code}: {response.text}")


# Custom exceptions
class QuotaExceededException(Exception):
    pass

class InvalidAPIKeyException(Exception):
    pass

class VideoNotFoundException(Exception):
    pass

class YouTubeServerException(Exception):
    pass
```


#### Endpoint 2: videos.list (Detailed Metadata)

**Purpose:** Get detailed metadata for videos (batch operation, up to 50 IDs).

**Implementation:**

```python
def youtube_videos_details(api_key: str, video_ids: List[str]) -> List[dict]:
    """
    Get detailed metadata for videos (batch).
    
    Args:
        api_key: YouTube Data API key
        video_ids: List of video IDs (max 50)
    
    Returns:
        List of video metadata dictionaries
    
    Quota Cost: 1 unit (regardless of number of IDs up to 50)
    """
    if len(video_ids) > 50:
        raise ValueError("Maximum 50 video IDs per request")
    
    url = 'https://www.googleapis.com/youtube/v3/videos'
    
    params = {
        'key': api_key,
        'part': 'snippet,statistics,contentDetails',
        'id': ','.join(video_ids)
    }
    
    response = requests.get(url, params=params, timeout=30)
    
    if response.status_code != 200:
        handle_youtube_api_error(response)
    
    data = response.json()
    videos = []
    
    for item in data.get('items', []):
        video = {
            'video_id': item['id'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'channel_id': item['snippet']['channelId'],
            'channel_title': item['snippet']['channelTitle'],
            'upload_date': item['snippet']['publishedAt'],
            'duration': item['contentDetails']['duration'],
            'category_id': item['snippet'].get('categoryId'),
            'views': int(item['statistics'].get('viewCount', 0)),
            'likes': int(item['statistics'].get('likeCount', 0)),
            'comments': int(item['statistics'].get('commentCount', 0)),
            'tags': item['snippet'].get('tags', []),  # UPDATED: Add tags for SEO/analysis
            'thumbnails': item['snippet']['thumbnails']
        }
        videos.append(video)
    
    return videos
```


#### Endpoint 3: channels.list (Channel Subscriber Count)

**Purpose:** Get channel subscriber count for V-Score calculation.

**Implementation:**

```python
def youtube_channel_subscribers(api_key: str, channel_id: str) -> int:
    """
    Get channel subscriber count.
    
    Args:
        api_key: YouTube Data API key
        channel_id: YouTube channel ID
    
    Returns:
        Subscriber count (integer)
    
    Quota Cost: 1 unit
    """
    url = 'https://www.googleapis.com/youtube/v3/channels'
    
    params = {
        'key': api_key,
        'part': 'statistics',
        'id': channel_id
    }
    
    response = requests.get(url, params=params, timeout=30)
    
    if response.status_code != 200:
        handle_youtube_api_error(response)
    
    data = response.json()
    
    if data.get('items'):
        stats = data['items']['statistics']
        return int(stats.get('subscriberCount', 0))
    
    return 0
```


#### Thumbnail Extraction (From API Response)

**Purpose:** Get highest quality thumbnail URL available.

**Implementation:**

```python
def extract_thumbnail(thumbnails_dict: dict) -> dict:
    """
    Extract best available thumbnail from API response.
    
    Args:
        thumbnails_dict: thumbnails object from YouTube API
    
    Returns:
        dict: {
            'url': str,
            'width': int,
            'height': int,
            'quality': str
        }
    
    Priority: maxres > standard > high > medium > default
    """
    quality_order = ['maxres', 'standard', 'high', 'medium', 'default']
    
    for quality in quality_order:
        if quality in thumbnails_dict:
            thumb = thumbnails_dict[quality]
            return {
                'url': thumb['url'],
                'width': thumb.get('width'),
                'height': thumb.get('height'),
                'quality': quality
            }
    
    # Fallback (should never happen)
    return {
        'url': f'https://i.ytimg.com/vi/default.jpg',
        'width': 120,
        'height': 90,
        'quality': 'default'
    }
```


---

### 7.2 Deepgram API

**Official Documentation:** https://developers.deepgram.com/docs

**Authentication:**

- Method: Bearer token (HTTP header: `Authorization: Token YOUR_KEY`)
- Obtain key: Deepgram Console > API Keys
- Pricing: ~\$0.0125 per minute
- Free tier: \$200 credit (~12,000 minutes)

**Model:** nova-2 (latest as of Feb 2026, best accuracy for English)

#### Implementation

```python
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import subprocess
import os
from typing import Optional

def deepgram_transcribe(video_url: str, api_key: str) -> str:
    """
    Transcribe YouTube video audio using Deepgram.
    
    Process:
    1. Download audio with yt-dlp (requires ffmpeg)
    2. Send to Deepgram API
    3. Extract transcript text
    4. Clean up temporary files
    
    Args:
        video_url: YouTube video URL
        api_key: Deepgram API key
    
    Returns:
        Transcript text (string)
    
    Raises:
        FileNotFoundError: If ffmpeg not installed
        DeepgramException: If transcription fails
    """
    # Step 1: Download audio
    audio_file = download_audio_ytdlp(video_url)
    
    try:
        # Step 2: Initialize Deepgram client
        deepgram = DeepgramClient(api_key)
        
        # Step 3: Read audio file
        with open(audio_file, 'rb') as audio:
            buffer_data = audio.read()
        
        payload: FileSource = {
            'buffer': buffer_data
        }
        
        # Step 4: Configure transcription options
        options = PrerecordedOptions(
            model='nova-2',  # Latest model (Feb 2026)
            language='en',
            punctuate=True,  # Add punctuation
            diarize=False,  # No speaker identification (not needed for faceless content)
            smart_format=True,  # Format dates, times, numbers
            utterances=False,  # Don't split by speaker
            paragraphs=False  # Return as continuous text
        )
        
        # Step 5: Transcribe
        response = deepgram.listen.rest.v('1').transcribe_file(payload, options)
        
        # Step 6: Extract transcript text
        transcript = response['results']['channels']['alternatives']['transcript']
        
        return transcript
    
    finally:
        # Step 7: Cleanup temporary audio file
        if os.path.exists(audio_file):
            os.remove(audio_file)


def download_audio_ytdlp(video_url: str) -> str:
    """
    Download audio from YouTube using yt-dlp.
    
    Args:
        video_url: YouTube video URL
    
    Returns:
        Path to downloaded audio file (.mp3)
    
    Raises:
        FileNotFoundError: If yt-dlp or ffmpeg not installed
        subprocess.CalledProcessError: If download fails
    
    Requirements:
        - yt-dlp installed: pip install yt-dlp
        - ffmpeg installed: choco install ffmpeg (Windows)
    """
    # Extract video ID for filename
    video_id = video_url.split('=')[-1].split('&')
    output_file = f'temp_audio_{video_id}.mp3'
    
    command = [
        'yt-dlp',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--audio-quality', '0',  # Best quality
        '--output', output_file,
        '--no-playlist',
        video_url
    ]
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            check=True
        )
        
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"yt-dlp failed to create audio file: {output_file}")
        
        return output_file
    
    except subprocess.TimeoutExpired:
        raise Exception(f"Audio download timeout after 5 minutes: {video_url}")
    
    except subprocess.CalledProcessError as e:
        if 'ffmpeg' in e.stderr.lower():
            raise FileNotFoundError(
                "ffmpeg not found. Install with: choco install ffmpeg"
            )
        raise Exception(f"yt-dlp download failed: {e.stderr}")


def ytdlp_extract_transcript_fallback(video_url: str) -> Optional[str]:
    """
    Fallback: Extract transcript using yt-dlp (YouTube auto-captions).
    
    This is FREE but less accurate than Deepgram.
    Use only when Deepgram quota exhausted or API fails.
    
    Args:
        video_url: YouTube video URL
    
    Returns:
        Transcript text or None if unavailable
    """
    video_id = video_url.split('=')[-1].split('&')
    transcript_file = f'temp_transcript_{video_id}.en.vtt'
    
    command = [
        'yt-dlp',
        '--skip-download',
        '--write-auto-sub',
        '--sub-lang', 'en',
        '--sub-format', 'vtt',
        '--output', f'temp_transcript_{video_id}',
        video_url
    ]
    
    try:
        subprocess.run(command, capture_output=True, text=True, check=True, timeout=60)
        
        if os.path.exists(transcript_file):
            with open(transcript_file, 'r', encoding='utf-8') as f:
                vtt_content = f.read()
            
            # Clean VTT format (remove timestamps, tags)
            transcript = clean_vtt_format(vtt_content)
            
            # Cleanup
            os.remove(transcript_file)
            
            return transcript
    
    except:
        pass
    
    return None


def clean_vtt_format(vtt_text: str) -> str:
    """Remove VTT formatting (timestamps, tags)."""
    import re
    
    # Remove WEBVTT header
    text = re.sub(r'WEBVTT.*?\n\n', '', vtt_text, flags=re.DOTALL)
    
    # Remove timestamps (00:00:00.000 --> 00:00:05.000)
    text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}', '', text)
    
    # Remove position/alignment tags
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)
    text = re.sub(r'align:start position:\d+%', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove multiple newlines
    text = re.sub(r'\n{2,}', '\n', text)
    
    return text.strip()
```


---

### 7.3 Gemini AI

**Official Documentation:** https://ai.google.dev/docs

**Authentication:**

- Method: API Key (SDK handles header automatically)
- Obtain key: Google AI Studio > Get API Key
- Model: `gemini-1.5-pro` (128K context window, multimodal)
- Pricing: Free tier 60 requests/minute


#### Implementation

```python
import google.generativeai as genai
import json
import html
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential

class GeminiClient:
    def __init__(self, api_key: str, config: dict):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(config['gemini']['model'])
        self.config = config
        self.banned_terms = config['gemini']['banned_terms']
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def classify_sub_niches_from_transcripts(
        self,
        category: str,
        transcripts: List[str],
        titles: List[str]
    ) -> Dict:
        """
        Classify 1000 transcripts into 5 specific sub-niches (Round 1).

        Args:
            category: Broad niche (e.g., "Horror")
            transcripts: 1000 cleaned video transcripts
            titles: 1000 video titles (for reference)

        Returns:
            dict: {
                'category': str,
                'sub_niches': [
                    {
                        'name': str,
                        'video_count': int,
                        'demand': 'High' | 'Medium' | 'Low',
                        'examples': [str, str, str]
                    },
                    ...
                ]
            }
        """
        safe_category = html.escape(category)

        # Prepare transcript snippets (first 200 words each for context)
        transcript_snippets = []
        for i, (title, transcript) in enumerate(zip(titles, transcripts)):
            safe_title = html.escape(title[:100])
            safe_transcript = html.escape(transcript[:200])  # First 200 words
            transcript_snippets.append(f"VIDEO {i+1}: {safe_title}\n{safe_transcript}")

        all_snippets = '\n\n---\n\n'.join(transcript_snippets[:1000])

        prompt = f"""<task>
You are a YouTube content analyst. Analyze these 1000 video transcripts from the category "{safe_category}" and identify the top 5 most dominant sub-niches (specific topic clusters).

ANALYSIS METHOD:
1. Read ALL transcript snippets to understand content themes
2. Cluster videos by similar topics/angles/approaches
3. Identify 5 distinct sub-niches with highest demand

For each sub-niche, provide:
1. Sub-niche name (2-4 words, specific, searchable keywords)
2. Video count (how many videos belong to this sub-niche)
3. Demand score (High if count > 200, Medium if 100-200, Low if < 100)
4. Example titles (3 representative video titles)

RULES:
- Sub-niches must be SPECIFIC (not broad)
- Focus on HIGH DEMAND topics (most videos cluster here)
- No overlap between sub-niches
- Sub-niche names should be YouTube search keywords
- Analyze FULL transcript content, not just titles

TRANSCRIPT SAMPLES (First 200 words each):
{all_snippets}

Output (JSON only, no markdown):
{{
  "category": "{safe_category}",
  "sub_niches": [
    {{"name": "...", "video_count": N, "demand": "High/Medium/Low", "examples": ["...", "...", "..."]}},
    ...
  ]
}}
</task>"""

        response = self.model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 2000
            }
        )

        # Parse JSON response
        try:
            result = json.loads(response.text)
            return result
        except json.JSONDecodeError:
            raise Exception("Gemini returned invalid JSON")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def classify_sub_niches(self, category: str, sample_titles: List[str]) -> Dict:
        """
        DEPRECATED: Use classify_sub_niches_from_transcripts() instead.
        This method is kept for backward compatibility.
        """
        pass
Output (JSON only, no markdown):
{{
  "category": "{safe_category}",
  "sub_niches": [
    {{"name": "...", "video_count": N, "demand": "High/Medium/Low", "examples": ["...", "...", "..."]}},
    ...
  ]
}}
</task>"""
        
        response = self.model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 1000
            }
        )
        
        # Parse JSON response
        try:
            result = json.loads(response.text)
            return result
        except json.JSONDecodeError:
            # Retry will be handled by @retry decorator
            raise Exception("Gemini returned invalid JSON")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def generate_titles(self, video_title: str, transcript_preview: str) -> List[str]:
        """
        Generate 3 click-magnet title variations.
        
        Args:
            video_title: Original competitor title
            transcript_preview: First 500 words of transcript
        
        Returns:
            List of 3 title variations
        """
        safe_title = html.escape(video_title)
        safe_transcript = html.escape(transcript_preview[:500])
        
        prompt = f"""<task>
You are a YouTube viral title specialist. Generate 3 click-magnet title variations for a faceless educational video.

Input Video Title (Competitor):
"{safe_title}"

Transcript Preview (First 500 words):
{safe_transcript}

Generate 3 title variations that:
1. Use psychological triggers (curiosity gap, shock, urgency)
2. Keep under 60 characters (mobile-friendly)
3. Include power words (Secret, Untold, Revealed, Hidden, Truth)
4. Avoid clickbait red flags (ALL CAPS, excessive punctuation)
5. Stay true to content (no misleading claims)

Output format (JSON):
{{
  "titles": [
    "Title variation 1",
    "Title variation 2",
    "Title variation 3"
  ]
}}
</task>

<examples>
Original: "The History of World War 2"
Generated:
1. "The Untold Secret That Changed WW2 Forever"
2. "What They Never Taught You About World War 2"
3. "The Hidden Truth Behind WW2's Biggest Mystery"
</examples>

<constraints>
- No banned terms: "subscribe", "like", "click", "comment", "bell icon"
- No exaggeration (avoid "INSANE", "SHOCKING" overuse)
- Factual accuracy (verifiable claims only)
</constraints>"""
        
        response = self.model.generate_content(
            prompt,
            generation_config={'temperature': 0.7, 'max_output_tokens': 200}
        )
        
        try:
            result = json.loads(response.text)
            return result['titles']
        except:
            # Fallback if JSON parsing fails
            return [video_title] * 3
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def generate_edsa_script(
        self,
        video_title: str,
        transcript_cleaned: str,
        chapters: List[Dict],
        duration_seconds: int
    ) -> str:
        """
        Generate EDSA script from competitor transcript.
        
        Args:
            video_title: Competitor title
            transcript_cleaned: Cleaned transcript (full)
            chapters: List of chapter dicts
            duration_seconds: Video duration
        
        Returns:
            EDSA script (string, 2000-5000 words)
        
        Raises:
            BannedTermsException: If script contains banned terms after 3 retries
        """
        safe_title = html.escape(video_title)
        safe_transcript = html.escape(transcript_cleaned)
        
        # Format chapters
        chapters_text = ""
        if chapters and len(chapters) > 0:
            chapters_text = "Chapter Breakdown:\n" + "\n".join([
                f"- {ch['timestamp']} {html.escape(ch['title'])}"
                for ch in chapters[:5]
            ])
        
        prompt = f"""<task>
Rewrite this competitor YouTube transcript into a NEW original EDSA script for faceless content.

EDSA Framework:
- E = Engage (Hook: First 5-10 seconds, open loop)
- D = Deliver (Main content: Educational value, storytelling)
- S = Sustain (Retention tactics: Mini-cliffhangers, callbacks)
- A = Amplify (Conclusion: Emotional peak, key takeaway)

Input Data:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Original Title: "{safe_title}"
Duration: {duration_seconds} seconds
{chapters_text}

Competitor Transcript (Cleaned):
{safe_transcript}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your Task:
1. HOOK (0-10 sec): Create urgent open loop (teaser, shocking fact, mystery)
2. STRUCTURE: Mimic competitor's chapter flow (intro, 3-5 sections, conclusion)
3. RETENTION: Add mini-hooks every 60-90 seconds ("But here's where it gets interesting...")
4. STORYTELLING: Transform facts into narrative (characters, conflict, resolution)
5. ORIGINALITY: Different words, same structure (avoid plagiarism)
6. LENGTH: Target {duration_seconds * 150} words (~150 words per minute voiceover)

Output: Full EDSA script (plain text, no markdown formatting)
</task>

<banned_terms>
DO NOT include these phrases (YouTube spam policy):
- "Subscribe to my channel"
- "Like this video"
- "Hit the bell icon"
- "Check the description"
- "Link in description below"
- "Comment below"
- "Smash that like button"
- "Don't forget to subscribe"
</banned_terms>

<example_hook>
BAD: "Hello everyone, today we're talking about World War 2..."
GOOD: "One decision in 1944 killed 50,000 soldiers in 24 hours. The generals knew it would fail. They sent them anyway. Here's why."
</example_hook>"""
        
        response = self.model.generate_content(
            prompt,
            generation_config={'temperature': 0.7, 'max_output_tokens': 8000}
        )
        
        script = response.text
        
        # Validate banned terms
        if not self._validate_banned_terms(script):
            raise BannedTermsException("Script contains banned terms")
        
        return script
    
    def _validate_banned_terms(self, text: str) -> bool:
        """Check if text contains banned terms."""
        text_lower = text.lower()
        for term in self.banned_terms:
            if term.lower() in text_lower:
                return False
        return True
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def generate_seo_description(
        self,
        title: str,
        script_preview: str
    ) -> Dict:
        """
        Generate SEO description and keywords.
        
        Args:
            title: Selected title (from title_options)
            script_preview: First 1000 words of EDSA script
        
        Returns:
            dict: {
                'description': str (150-200 words),
                'keywords': list (10 keywords)
            }
        """
        safe_title = html.escape(title)
        safe_script = html.escape(script_preview[:1000])
        
        prompt = f"""<task>
Generate YouTube video description optimized for search ranking.

Input:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Video Title: "{safe_title}"
Script Preview (First 1000 words):
{safe_script}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generate:
1. Description (150-200 words):
   - First 2-3 sentences: Hook + video summary
   - Middle: Key points covered (bullet points)
   - End: Call to curiosity (not subscribe CTA)

2. Keywords (10 keywords):
   - Mix of broad + long-tail keywords
   - Relevant to video content
   - High search volume potential

Output format (JSON):
{{
  "description": "Full description text...",
  "keywords": ["keyword1", "keyword2", ..., "keyword10"]
}}
</task>"""
        
        response = self.model.generate_content(
            prompt,
            generation_config={'temperature': 0.7, 'max_output_tokens': 500}
        )
        
        try:
            return json.loads(response.text)
        except:
            return {
                'description': f"Watch this video about {title}",
                'keywords': [title.lower()]
            }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def generate_thumbnail_prompt(self, title: str, thumbnail_url: str) -> str:
        """
        Generate thumbnail description for AI image generation.
        
        Args:
            title: Video title
            thumbnail_url: Competitor thumbnail URL (for reference)
        
        Returns:
            Text prompt for Midjourney/DALL-E
        """
        safe_title = html.escape(title)
        
        prompt = f"""<task>
Create a detailed prompt for AI image generation (Midjourney/DALL-E) to create a YouTube thumbnail.

Video Title: "{safe_title}"
Competitor Thumbnail: {thumbnail_url} (for style reference)

Describe visual elements for thumbnail that:
1. HIGH CONTRAST: Bold colors, clear focal point
2. CURIOSITY GAP: Visual teaser (mysterious object, dramatic scene)
3. TEXT OVERLAY: 3-5 words max (large, readable font)
4. EMOTIONAL TRIGGER: Shock, awe, intrigue
5. MINIMALIST: One main subject, simple background

Output format (plain text description for Midjourney/DALL-E):
Describe foreground, background, color scheme, text overlay, composition.
</task>

<example_output>
"Foreground: Close-up of a rusted World War 2 tank barrel pointing directly at camera, dramatic angle. Background: Blurred smoke and fire, dark grey tones with orange highlights. Color scheme: Desaturated war tones (grey, brown, orange fire glow). Text overlay: Large bold white text 'THE SECRET WEAPON' with slight shadow for readability, positioned top-right. Composition: Rule of thirds, tank barrel occupies left 2/3 of frame, text balances right side. Lighting: Cinematic rim lighting on tank metal, high contrast shadows. Mood: Intense, mysterious, historical drama. Style: Photorealistic documentary thumbnail."
</example_output>"""
        
        response = self.model.generate_content(
            prompt,
            generation_config={'temperature': 0.7, 'max_output_tokens': 300}
        )
        
        return response.text


class BannedTermsException(Exception):
    pass
```


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

## 9. MACHINE LEARNING PIPELINE

### Feature Engineering

**Raw YouTube Features:**

- views (integer)
- likes (integer)
- comments (integer)
- subscriber_count (integer)
- upload_date (timestamp)

**Calculated Features:**

```python
# Primary viral indicator
v_score = views / subscriber_count

# Engagement metrics
like_view_ratio = likes / views
comment_view_ratio = comments / views
engagement_rate = (likes + comments) / views

# Temporal features
upload_age_days = (today - upload_date).days
viral_velocity = views / upload_age_days
```

**Feature Importance Ranking:**


| Feature | Weight | Justification |
| :-- | :-- | :-- |
| v_score | 50% | Primary indicator of organic virality (high views despite low subs) |
| engagement_rate | 30% | Measures audience interaction quality |
| viral_velocity | 20% | Indicates momentum (fast growth = trending content) |


---

### Isolation Forest (Stage 3)

**Algorithm:** Anomaly detection via isolation

**How It Works:**

- Build ensemble of random decision trees
- Anomalies (outliers) are isolated faster (require fewer splits)
- Videos with abnormally high V-Scores are classified as outliers

**Hyperparameters:**

```python
contamination=0.1      # Expect 10% of data to be outliers (~50 from 500)
random_state=42        # Reproducible results (same input = same output)
n_estimators=100       # Number of trees in ensemble
max_features=1.0       # Use all features
bootstrap=False        # Use full dataset per tree
```

**Input Features:** `[v_score, views, upload_age_days]`

**Output:** Binary classification (1 = inlier, -1 = outlier)

**Expected Result:** 500 videos → ~50 outlier candidates

---

### DBSCAN (Stage 4)

**Algorithm:** Density-based clustering

**How It Works:**

- Identify high-density clusters (normal viral videos with similar patterns)
- Points that don't belong to any cluster = NOISE (true outliers)
- Noise points have unique engagement patterns (organic viral, not paid promotion)

**Hyperparameters:**

```python
eps=0.5                # Neighborhood radius (distance threshold)
min_samples=3          # Minimum points to form cluster
metric='euclidean'     # Distance metric
```

**Input Features:** `[like_view_ratio, comment_view_ratio, v_score]` (StandardScaled)

**Output:** Cluster labels (0, 1, 2... = cluster ID, -1 = noise/outlier)

**Expected Result:** 50 candidates → ~10-15 true outliers

---

### Adaptive Thresholding (Per-Niche Calibration)

Different niches have different "normal" V-Score distributions:

```python
def calculate_adaptive_contamination(videos_df):
    """
    Adjust Isolation Forest contamination based on niche variance.
    
    Logic:
    - High variance niche → More outliers expected → Higher contamination
    - Low variance niche → Fewer outliers expected → Lower contamination
    """
    v_scores = videos_df['v_score']
    
    median = v_scores.median()
    p90 = v_scores.quantile(0.90)
    variance_ratio = p90 / median
    
    if variance_ratio > 5:
        # High variance (e.g., Tech reviews, Gaming)
        contamination = 0.15
    elif variance_ratio > 3:
        # Medium variance (e.g., Education, Finance)
        contamination = 0.10
    else:
        # Low variance (e.g., Music covers, ASMR)
        contamination = 0.08
    
    return contamination
```

**Example Niche Profiles:**


| Niche | Median V-Score | P90 V-Score | Variance Ratio | Contamination |
| :-- | :-- | :-- | :-- | :-- |
| History Docs | 3.5 | 18.2 | 5.2 | 0.15 (high variance) |
| Tech Reviews | 2.8 | 9.4 | 3.4 | 0.10 (medium variance) |
| ASMR | 4.2 | 8.1 | 1.9 | 0.08 (low variance) |


---

### Hard Filter Rules (Updated)

**Criteria:**

| Rule | Value | Purpose |
| :-- | :-- | :-- |
| subscriber_count | <= 30,000 | Small channels only (viral potential) |
| views | >= 50,000 | Minimum viral threshold |
| views | <= subscriber_count × 50 | Anti-paid promotion (organic viral only) |
| upload_age_days | >= 7 | Exclude brand new videos |
| upload_age_days | <= 21 | Recent viral only (max 3 weeks) |

**Views/Subs Ratio Examples:**

| Subscribers | Views | Ratio (views/subs) | Status |
| :-- | :-- | :-- | :-- |
| 1,000 | 50,000 | 50x | ✅ Valid (at threshold) |
| 1,000 | 200,000 | 200x | ❌ Paid promotion (exceeds 50x) |
| 5,000 | 50,000 | 10x | ✅ Valid |
| 5,000 | 500,000 | 100x | ❌ Paid promotion |
| 10,000 | 100,000 | 10x | ✅ Valid |
| 10,000 | 2,000,000 | 200x | ❌ Paid promotion |


---

## 10. USER INTERFACE DESIGN

### Design System

**Color Palette:**

```python
# Light Mode (Default)
COLOR_BACKGROUND = "#FCFCF9"
COLOR_SURFACE = "#FFFFFE"
COLOR_TEXT = "#13343B"
COLOR_TEXT_SECONDARY = "#626C71"
COLOR_PRIMARY = "#21808D"
COLOR_PRIMARY_HOVER = "#1D7480"
COLOR_SUCCESS = "#21808D"
COLOR_ERROR = "#C0152F"
COLOR_WARNING = "#A84B2F"
COLOR_BORDER = "rgba(94,82,64,0.2)"

# Dark Mode (Auto-detect system theme)
COLOR_BACKGROUND_DARK = "#1F2121"
COLOR_SURFACE_DARK = "#262828"
COLOR_TEXT_DARK = "#F5F5F5"
COLOR_PRIMARY_DARK = "#32B8C6"
```

**Typography:**

```python
FONT_FAMILY = "Segoe UI"
FONT_SIZE_TITLE = 18
FONT_SIZE_SECTION = 14
FONT_SIZE_LABEL = 11
FONT_SIZE_INPUT = 12
FONT_SIZE_BUTTON = 12
FONT_SIZE_LOG = 10
```

**Layout Constants:**

```python
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
PADDING = 20
PADDING_SMALL = 10
INPUT_HEIGHT = 40
BUTTON_HEIGHT = 45
PROGRESS_BAR_HEIGHT = 25
LOG_BOX_HEIGHT = 180
```


---

### Screen Flow (7 Steps)

**Step 1: Category \& Sub-Niche Selection**

```
Category Input Field
    ↓
[ANALISIS SUB-NICHE Button]
    ↓
5 Radio Buttons (sub-niche options)
    ↓
Target Video Count Dropdown
    ↓
[LANJUT KE SCRAPING Button]
```

**Step 2-7:** Progress screens with real-time logging

---

### Lucide Icons (Embedded PNG Files)

**Complete Icon List:**


| Icon File | Size | Color | Use Case |
| :-- | :-- | :-- | :-- |
| `check-circle-green.png` | 20x20 | \#32A852 | Success indicators |
| `alert-triangle-orange.png` | 20x20 | \#FFA500 | Warning messages |
| `x-circle-red.png` | 20x20 | \#E74C3C | Error messages |
| `info-blue.png` | 20x20 | \#3498DB | Info messages |
| `loader-blue.gif` | 20x20 | \#3498DB (animated) | Processing state |
| `key-grey.png` | 20x20 | \#9D9D9D | API key status |
| `database-grey.png` | 20x20 | \#9D9D9D | Database operations |
| `file-spreadsheet-green.png` | 24x24 | \#32A852 | Export success |

**Loading Icons:**

```python
from PIL import Image
import customtkinter as ctk

def load_icon(filename: str) -> ctk.CTkImage:
    """Load icon from assets/icons/ directory."""
    image = Image.open(f"assets/icons/{filename}")
    return ctk.CTkImage(light_image=image, dark_image=image, size=(20, 20))

# Load all icons at startup
ICONS = {
    "check": load_icon("check-circle-green.png"),
    "warning": load_icon("alert-triangle-orange.png"),
    "error": load_icon("x-circle-red.png"),
    "info": load_icon("info-blue.png"),
    "loader": load_icon("loader-blue.gif"),
    "key": load_icon("key-grey.png"),
    "database": load_icon("database-grey.png"),
    "export": load_icon("file-spreadsheet-green.png")
}
```

**Fallback Strategy:**

```python
def load_icon_with_fallback(filename: str) -> ctk.CTkImage:
    """Load icon with fallback to placeholder if file missing."""
    try:
        image = Image.open(f"assets/icons/{filename}")
        return ctk.CTkImage(light_image=image, dark_image=image, size=(20, 20))
    except FileNotFoundError:
        # Create placeholder (solid color square)
        placeholder = Image.new('RGB', (20, 20), color='#626C71')
        return ctk.CTkImage(light_image=placeholder, dark_image=placeholder, size=(20, 20))
```


---

## 11. DATA FLOW \& STATE MANAGEMENT

### State Machine

```
RAW (Initial state after scraping)
 ↓
 [Sanitizer Module]
 ↓
CLEANED (Transcript cleaned, quality >= 50)
 ↓
 [Geo-Validator Module]
 ↓
tier1_validated=1 (Passed Tier 1 filtering)
 ↓
 [Analyst Module]
 ↓
OUTLIER (Top 10 by composite score)
 ↓
 [Architect Module]
 ↓
READY (All AI content generated)
 ↓
 [Exporter Module]
 ↓
EXPORTED (Included in Excel output)

FAILED (Can transition from any state if error occurs)
```


---

### State Transition Rollback Strategy

**Scenario 1: Module Fails Mid-Processing**

```python
# Example: Architect module fails on video #6 of 10

def handle_module_failure(module_name, video_id, error):
    """
    Handle module failure with rollback option.
    
    Strategy:
    1. Log error to processing_log table
    2. Mark video as state='FAILED'
    3. Continue processing remaining videos
    4. Partial success: Export what's available
    """
    log_error(module_name, f"Failed on {video_id}: {error}")
    
    # Update video state
    video = Video.get(video_id=video_id)
    video.state = 'FAILED'
    video.error_message = str(error)
    video.save()
    
    # Continue with next video (no full rollback)
    return 'continue'
```

**Scenario 2: User Stops Mid-Scraping**

```python
def handle_user_interrupt():
    """
    Handle user clicking 'Cancel' button mid-scraping.
    
    Strategy:
    1. Stop current operation gracefully
    2. Save progress (videos scraped so far remain in database)
    3. No rollback (allow resume from last position)
    4. Next run: Skip videos already in database
    """
    log_warning("controller", "User interrupted scraping")
    
    # Set flag to stop loop
    global scraping_active
    scraping_active = False
    
    # Database state preserved (no deletion)
    # Next run will query: SELECT COUNT(*) WHERE state != 'FAILED'
    # And scrape remaining videos to reach target count
```

**Scenario 3: Partial Success (8/10 Videos Ready)**

```python
def handle_partial_success(ready_videos, failed_videos):
    """
    Handle partial success in Architect module.
    
    Strategy:
    1. Export available videos (8 in this case)
    2. Log summary (8 success, 2 failed)
    3. User can optionally retry failed videos
    4. No blocking (proceed with what's available)
    """
    if len(ready_videos) >= 5:
        # Minimum threshold met (at least 5 videos)
        log_info("controller", f"Partial success: {len(ready_videos)} ready, {len(failed_videos)} failed")
        
        # Proceed to export
        exporter.export_to_excel(ready_videos, sub_niche)
        
        return 'export_partial'
    else:
        # Below minimum threshold
        log_error("controller", f"Insufficient videos ready: {len(ready_videos)}")
        
        return 'retry_failed'
```


---

## 12. ERROR HANDLING \& RECOVERY

### Always/Ask/Never Boundaries

**ALWAYS:**

- Retry API calls 3x with exponential backoff [2s, 4s, 8s]
- Log errors to processing_log table with full context
- Update video state to 'FAILED' after max retries
- Sanitize user input before sending to external APIs (HTML escape)
- Use parameterized SQL queries (prevent injection)
- Validate API key status before making requests
- Apply rate limiting between API calls
- Handle edge cases (division by zero, empty strings, None values)

**ASK FIRST:**

- If database schema changes needed (confirm with developer)
- If adding new external dependencies (confirm compatibility)
- If changing ML hyperparameters (verify impact on accuracy)
- If modifying state transition logic (ensure no deadlocks)

**NEVER:**

- Hardcode API keys in source files
- Use browser storage APIs (localStorage, sessionStorage) - they fail in sandbox
- Skip data validation before database insert
- Ignore API quota limits (always check before request)
- Modify original raw data (preserve transcript_raw, keep cleaned separate)
- Proceed with quality score < 50 (minimum threshold)
- Generate code with placeholders (all functionality must be complete)

---

### Retry Logic (Decorator Pattern)

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import requests

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=8),
    retry_if=retry_if_exception_type((requests.exceptions.RequestException, TimeoutError)),
    reraise=True
)
def api_call_with_retry(url, params):
    """
    API call with automatic retry.
    
    Retry behavior:
    - Attempt 1: Immediate
    - Attempt 2: Wait 2 seconds
    - Attempt 3: Wait 4 seconds
    - Attempt 4: Wait 8 seconds (max)
    - After 3 failures: Raise exception
    
    Only retries on: Network errors, timeouts
    Does NOT retry on: 4xx errors (client errors)
    """
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    return response.json()
```


---

### Error Categories \& Handling

| Error Type | Detection | Handling Strategy | Retry? |
| :-- | :-- | :-- | :-- |
| **API Quota Exceeded** | HTTP 403 + reason='quotaExceeded' | Rotate to next API key, log event | No (use next key) |
| **Invalid API Key** | HTTP 403 + reason='forbidden' | Mark key as 'INVALID', notify user | No (skip key) |
| **Rate Limit (429)** | HTTP 429 | Exponential backoff, retry | Yes (3x) |
| **Server Error (500)** | HTTP 500-599 | Log error, retry with delay | Yes (3x) |
| **Network Timeout** | requests.Timeout | Increase timeout, retry | Yes (3x) |
| **Video Unavailable** | HTTP 404 | Log as 'VIDEO_NOT_FOUND', skip | No (skip video) |
| **Transcript Missing** | Deepgram fail + yt-dlp fail | Log as 'NO_TRANSCRIPT', mark FAILED | No (skip video) |
| **Banned Terms Detected** | Regex match in script | Retry Gemini with stricter prompt | Yes (3x max) |
| **Quality Score < 50** | Calculated in Sanitizer | Mark state='FAILED', log reason | No (validation failure) |
| **Division by Zero** | Math operation | Replace with 0, log warning | No (handle edge case) |


---

## 13. LOGGING STRATEGY

### Log Levels

| Level | Use Case | Example |
| :-- | :-- | :-- |
| **DEBUG** | Development debugging, trace execution flow | "Entering function: scrape_videos()" |
| **INFO** | Normal operation, progress updates | "Scraped 542/1000 videos" |
| **WARNING** | Recoverable issues, degraded performance | "YouTube key \#1 quota 85% full, rotating..." |
| **ERROR** | Operation failed, but app continues | "Failed to transcribe video abc123: Deepgram timeout" |
| **CRITICAL** | System failure, app cannot continue | "No active API keys available, stopping" |

### Logging Implementation

```python
# hunterbot/utils/logger.py

import sqlite3
import json
from datetime import datetime
from typing import Optional

def log(level: str, module: str, message: str, video_id: Optional[str] = None, context: Optional[dict] = None):
    """
    Log event to processing_log table.
    
    Args:
        level: "DEBUG" | "INFO" | "WARNING" | "ERROR" | "CRITICAL"
        module: Module name (e.g., "hunter", "sanitizer", "analyst")
        message: Log message (string)
        video_id: Optional video_id for context
        context: Optional additional data (dict, will be JSON serialized)
    """
    db_path = "hunterbot.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    context_json = json.dumps(context) if context else None
    
    cursor.execute("""
        INSERT INTO processing_log (module, level, message, video_id, context)
        VALUES (?, ?, ?, ?, ?)
    """, (module, level, message, video_id, context_json))
    
    conn.commit()
    conn.close()
    
    # Also print to console (development mode)
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] [{module}] {message}")


# Convenience functions
def log_debug(module: str, message: str, **kwargs):
    log("DEBUG", module, message, **kwargs)

def log_info(module: str, message: str, **kwargs):
    log("INFO", module, message, **kwargs)

def log_warning(module: str, message: str, **kwargs):
    log("WARNING", module, message, **kwargs)

def log_error(module: str, message: str, **kwargs):
    log("ERROR", module, message, **kwargs)

def log_critical(module: str, message: str, **kwargs):
    log("CRITICAL", module, message, **kwargs)
```


### Log Rotation (Prevent Database Bloat)

```python
def rotate_logs(keep_days: int = 30):
    """
    Delete old log entries to prevent database bloat.
    
    Args:
        keep_days: Number of days to keep logs (default 30)
    """
    from datetime import timedelta
    
    cutoff_date = (datetime.now() - timedelta(days=keep_days)).isoformat()
    
    conn = sqlite3.connect("hunterbot.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        DELETE FROM processing_log
        WHERE timestamp < ?
    """, (cutoff_date,))
    
    deleted_count = cursor.rowcount
    conn.commit()
    conn.close()
    
    log_info("system", f"Log rotation: Deleted {deleted_count} entries older than {keep_days} days")


# Run rotation on app startup
if __name__ == '__main__':
    rotate_logs(keep_days=30)
```


### Export Logs (Troubleshooting)

```python
def export_logs_to_file(output_path: str, level_filter: Optional[str] = None):
    """
    Export logs to text file for troubleshooting.
    
    Args:
        output_path: Output file path (e.g., "logs_export.txt")
        level_filter: Optional level filter ("ERROR", "WARNING", etc.)
    """
    conn = sqlite3.connect("hunterbot.db")
    cursor = conn.cursor()
    
    query = "SELECT timestamp, level, module, message, video_id FROM processing_log"
    
    if level_filter:
        query += f" WHERE level = '{level_filter}'"
    
    query += " ORDER BY timestamp DESC"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for row in rows:
            timestamp, level, module, message, video_id = row
            line = f"[{timestamp}] [{level}] [{module}] {message}"
            if video_id:
                line += f" (video: {video_id})"
            f.write(line + "\n")
    
    conn.close()
    
    log_info("system", f"Exported {len(rows)} log entries to {output_path}")
```


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

## 16. DEPLOYMENT GUIDE

### Nuitka Compilation

**Why Nuitka:**

- Compile Python to native executable (.exe)
- No Python installation required on user machine
- Faster startup than PyInstaller
- Better performance (C-level compilation)

**Build Script:**

```python
# build.py

import subprocess
import os
import sys

def build_executable():
    """
    Compile Hunterbot to Windows .exe using Nuitka.
    
    Requirements:
    - Nuitka installed: pip install nuitka
    - MSVC (Microsoft Visual C++) compiler installed
    - ffmpeg.exe in project directory (for bundling)
    """
    
    print("Building Hunterbot.exe with Nuitka...")
    
    command = [
        sys.executable, '-m', 'nuitka',
        '--standalone',                         # Include all dependencies
        '--onefile',                            # Single executable file
        '--windows-disable-console',            # No console window (GUI app)
        '--enable-plugin=tk-inter',             # Support CustomTkinter
        '--include-data-dir=assets=assets',     # Bundle assets folder
        '--include-data-file=ffmpeg.exe=ffmpeg.exe',  # Bundle ffmpeg
        '--include-package=sklearn',            # Include scikit-learn
        '--include-package=pandas',             # Include pandas
        '--include-package=deepgram',           # Include Deepgram SDK
        '--include-package=google',             # Include Google APIs
        '--output-dir=dist',                    # Output directory
        '--output-filename=Hunterbot.exe',      # Executable name
        '--company-name=Hunterbot',
        '--product-name=Hunterbot',
        '--file-version=2.0.0',
        '--product-version=2.0.0',
        '--file-description=YouTube Reverse Engineering Bot',
        'hunterbot/main.py'                     # Entry point
    ]
    
    print(f"Command: {' '.join(command)}\n")
    
    result = subprocess.run(command)
    
    if result.returncode == 0:
        print("\n" + "="*60)
        print("BUILD SUCCESSFUL!")
        print("="*60)
        print(f"Executable: dist/Hunterbot.exe")
        print(f"Size: ~{os.path.getsize('dist/Hunterbot.exe') // 1024 // 1024} MB")
    else:
        print("\n" + "="*60)
        print("BUILD FAILED!")
        print("="*60)
        sys.exit(1)

if __name__ == '__main__':
    build_executable()
```

**Run Build:**

```bash
python build.py
```

**Expected Output:**

- `dist/Hunterbot.exe` (single file, ~80-120MB)
- No external dependencies required (all bundled)

---

### First-Run Setup Wizard

**On first launch, guide user through API key setup:**

```python
# hunterbot/ui/setup_wizard.py

import customtkinter as ctk

class SetupWizard:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Hunterbot - First Time Setup")
        self.window.geometry("600x500")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create setup UI."""
        title = ctk.CTkLabel(
            self.window,
            text="Welcome to Hunterbot!",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(
            self.window,
            text="Let's set up your API keys to get started.",
            font=("Segoe UI", 12)
        )
        subtitle.pack(pady=10)
        
        # YouTube API Keys Section
        youtube_frame = ctk.CTkFrame(self.window)
        youtube_frame.pack(pady=20, padx=20, fill="both")
        
        ctk.CTkLabel(
            youtube_frame,
            text="YouTube Data API Keys",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)
        
        self.youtube_entries = []
        for i in range(5):
            entry = ctk.CTkEntry(
                youtube_frame,
                placeholder_text=f"YouTube API Key {i+1}",
                width=400
            )
            entry.pack(pady=5)
            self.youtube_entries.append(entry)
        
        # Similar sections for Deepgram and Gemini
        
        # Save button
        save_btn = ctk.CTkButton(
            self.window,
            text="Save & Start",
            command=self.save_keys,
            height=45
        )
        save_btn.pack(pady=20)
    
    def save_keys(self):
        """Save API keys to database."""
        # Validate keys (test with API call)
        # Save to api_keys table
        # Close wizard, launch main app
        pass
    
    def run(self):
        self.window.mainloop()
```


---

### File Structure (Complete)

```
hunterbot/
├── hunterbot/
│   ├── __init__.py
│   ├── main.py                  # Entry point
│   ├── config.py                # Config management
│   ├── database/
│   │   ├── __init__.py
│   │   ├── schema.py            # SQL schema
│   │   └── models.py            # ORM models
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── classifier.py
│   │   ├── hunter.py
│   │   ├── sanitizer.py
│   │   ├── geo_validator.py
│   │   ├── analyst.py
│   │   ├── architect.py
│   │   ├── exporter.py
│   │   └── guardian.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── controller.py
│   │   ├── setup_wizard.py
│   │   └── screens/
│   │       ├── __init__.py
│   │       ├── step1_category.py
│   │       ├── step2_scraping.py
│   │       ├── step3_transcript.py
│   │       ├── step4_filtering.py
│   │       ├── step5_generation.py
│   │       └── step6_export.py
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       ├── logger.py
│       └── helpers.py
├── assets/
│   └── icons/
│       ├── check-circle-green.png
│       ├── alert-triangle-orange.png
│       ├── x-circle-red.png
│       ├── info-blue.png
│       ├── loader-blue.gif
│       ├── key-grey.png
│       ├── database-grey.png
│       └── file-spreadsheet-green.png
├── tests/
│   ├── __init__.py
│   ├── test_hunter.py
│   ├── test_sanitizer.py
│   ├── test_analyst.py
│   └── fixtures/
│       └── videos_sample.csv
├── exports/                     # Excel output directory
├── requirements.txt
├── build.py                     # Nuitka build script
├── setup_dependencies.bat       # Dependency installer
├── .env.example                 # API key template
└── README.md
```


---

## 17. CODE GENERATION INSTRUCTIONS

### For AI Code Generation Agents

**IMPORTANT: Read this section before generating code.**

**Verification Checklist (MANDATORY):**

After generating each module, verify:

**Imports:**

- [ ] All imports at top of file (PEP 8 compliant)
- [ ] Absolute imports from `hunterbot.*` (not relative imports)
- [ ] No circular imports (check dependency graph)
- [ ] All imported modules exist in requirements.txt

**Error Handling:**

- [ ] All external API calls wrapped in try/except
- [ ] All database operations use parameterized queries (SQL injection prevention)
- [ ] All user inputs sanitized before processing (HTML escape)
- [ ] @retry decorator used for network calls

**Type Safety:**

- [ ] All function signatures have type hints
- [ ] Return types explicitly declared
- [ ] No implicit None returns

**Testing:**

- [ ] Each public function has docstring with example
- [ ] Edge cases documented (empty input, None values, division by zero)

**Logging:**

- [ ] All state transitions logged
- [ ] Errors logged with video_id context
- [ ] Progress logged at regular intervals (every 50 videos)

**Database:**

- [ ] All queries use parameterized format (?, ?)
- [ ] JSON fields use json.dumps() on insert, json.loads() on retrieve
- [ ] Timestamps use ISO 8601 format

**Configuration:**

- [ ] All magic numbers moved to config
- [ ] No hardcoded API keys
- [ ] All paths use os.path.join() for cross-platform compatibility

---

### Code Style Guidelines

**Naming Conventions:**

- Classes: `PascalCase` (e.g., `HunterModule`)
- Functions/methods: `snake_case` (e.g., `scrape_videos()`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `COLOR_PRIMARY`)
- Private methods: `_leading_underscore` (e.g., `_clean_transcript()`)

**Docstring Format:**

```python
def function_name(arg1: str, arg2: int = 10) -> dict:
    """
    One-line summary of function purpose.
    
    Detailed description (if needed). Explain complex logic,
    assumptions, or important side effects.
    
    Args:
        arg1: Description of arg1
        arg2: Description of arg2 (default: 10)
    
    Returns:
        dict: Description of return value structure
        Example: {'key': 'value', 'count': 42}
    
    Raises:
        ValueError: If arg1 is empty
        APIException: If external API call fails
    
    Example:
        >>> result = function_name("test", 20)
        >>> print(result['count'])
        20
    """
    pass
```


---

### Module Generation Order

**Generate modules in this sequence (dependencies first):**

1. `utils/logger.py` (no dependencies)
2. `utils/validators.py` (no dependencies)
3. `database/schema.py` (no dependencies, pure SQL)
4. `database/models.py` (depends on schema)
5. `modules/guardian.py` (depends on database, logger)
6. `modules/classifier.py` (depends on guardian)
7. `modules/hunter.py` (depends on guardian)
8. `modules/sanitizer.py` (depends on validators)
9. `modules/geo_validator.py` (depends on validators)
10. `modules/analyst.py` (depends on database)
11. `modules/architect.py` (depends on guardian)
12. `modules/exporter.py` (depends on database)
13. `ui/controller.py` (depends on all modules)
14. `ui/screens/*.py` (depends on controller)
15. `main.py` (entry point, depends on ui)

---

## 18. APPENDIX: DECISION LOG

### Critical Architecture Decisions (With Justification)

**1. No Proxy Usage**

**Decision:** Do NOT use proxies (residential or datacenter) for API calls.

**Reasoning:**

- YouTube Data API \& Deepgram API are official APIs
- Rate limiting is quota-based (tracked by API key), NOT IP-based
- Proxies cost \$50-100/month, provide ZERO benefit for official API endpoints
- API key rotation (free) achieves same goal with better reliability

**Evidence:** YouTube API documentation confirms quota tracking by project/key, not IP address.

**Implementation Impact:** Guardian module handles key rotation, no proxy code needed.

---

**2. Lucide Icons (Embedded PNG Method)**

**Decision:** Use Lucide icons as pre-generated PNG files, embedded in `assets/icons/`.

**Reasoning:**

- Lucide doesn't have Python bindings (is SVG-based JavaScript library)
- Runtime SVG → PNG conversion (cairosvg) adds dependency bloat + slower startup
- Embedding

<div align="center">⁂</div>

[^1]: PRD-YOUTUBE.md

[^2]: Full-Version-YouTube-Faceless-10-Juta-Pertama-Panduan-AI-Step-by-Step-untuk-Pemula-dari-Nol.pdf.pdf

[^3]: https://lirias.kuleuven.be/retrieve/658326

[^4]: https://stackoverflow.com/questions/78729816/how-to-minimize-youtube-data-api-v3-query-quota-useage

[^5]: https://www.youtube.com/watch?v=93DwLV0TkNs

