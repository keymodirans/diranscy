# 02 ARCHITECTURE

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

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

