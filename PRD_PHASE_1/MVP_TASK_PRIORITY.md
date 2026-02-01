# HUNTERBOT - MVP TASK PRIORITY

**Version:** 1.0
**Created:** February 1, 2026
**Purpose:** Define MVP roadmap for fastest working version

---

## MVP DEFINITION

**Minimum Viable Product:** Hunterbot yang bisa:
1. User input category (e.g., "Horror")
2. Scrapes video metadata from YouTube (100 videos for MVP)
3. Displays results in a table
4. Saves to SQLite database

**Post-MVP:** Add ML, AI, and advanced features incrementally

---

## PRIORITY SYSTEM

```
P0 (CRITICAL) - Must have for MVP to work
P1 (HIGH)     - Important but can defer to v1.1
P2 (MEDIUM)   - Nice to have, can defer to v1.2+
P3 (LOW)      - Future enhancement
```

---

## TASK LIST (Priority Order)

### PHASE 1: FOUNDATION (P0)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P0-1: PROJECT SKELETON                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 2 hours                                                          │
│  Dependencies: None                                                        │
│  Output: Basic project structure                                          │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Create project folder structure                                   │
│  - [ ] Setup virtual environment                                         │
│  - [ ] Create requirements.txt (minimal)                                  │
│  - [ ] Create main.py entry point                                        │
│  - [ ] Test basic Python + CustomTkinter setup                          │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/                                                             │
│    ├── __init__.py                                                       │
│    ├── main.py                                                           │
│    ├── config.py                                                         │
│    └── requirements.txt                                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P0-2: DATABASE SETUP                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 2 hours                                                          │
│  Dependencies: P0-1                                                        │
│  Output: Working SQLite database                                          │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Create database/schema.py                                          │
│  - [ ] Create database/models.py                                         │
│  - [ ] Implement video table (minimal columns)                           │
│  - [ ] Test database creation and connection                             │
│                                                                             │
│  Minimal video table:                                                     │
│  - id, video_id, title, channel_title, views, upload_date                 │
│  - thumbnail_url, state, created_at                                     │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/database/__init__.py                                        │
│  - hunterbot/database/schema.py                                           │
│  - hunterbot/database/models.py                                           │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P0-3: BASIC UI FRAMEWORK                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 3 hours                                                          │
│  Dependencies: P0-1                                                        │
│  Output: Working CustomTkinter window                                     │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Create main window (800x600)                                       │
│  - [ ] Add title label                                                    │
│  - [ ] Add category input field                                            │
│  - [ ] Add "Start Scraping" button                                        │
│  - [ ] Add progress label                                                 │
│  - [ ] Add results table (CustomTkinter CTkTable)                        │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/ui/__init__.py                                               │
│  - hunterbot/ui/main_window.py                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P0-4: YOUTUBE API INTEGRATION (METADATA ONLY)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 4 hours                                                          │
│  Dependencies: P0-2, P0-3                                                  │
│  Output: Can fetch video metadata from YouTube                             │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Setup YouTube Data API v3 client                                   │
│  - [ ] Implement youtube_search() function                               │
│  - [ ] Implement youtube_videos_details() function                       │
│  - [ ] Test with API key                                                  │
│  - [ ] Fetch 10 videos as proof of concept                               │
│                                                                             │
│  MVP Limitation: Only metadata, no transcripts                          │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/api/youtube_api.py                                           │
│  - hunterbot/modules/hunter.py                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P0-5: SCRAPING ORCHESTRATION                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 3 hours                                                          │
│  Dependencies: P0-4                                                        │
│  Output: Can scrape N videos and save to DB                               │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Implement scrape_videos() function                                │
│  - [ ] Save metadata to database                                           │
│  - [ ] Update UI with progress                                             │
│  - [ ] Handle errors gracefully                                           │
│                                                                             │
│  MVP Limitation: Only 100 videos (not 1000)                              │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/modules/hunter.py                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P0-6: UI RESULTS DISPLAY                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 2 hours                                                          │
│  Dependencies: P0-5                                                        │
│  Output: Display scraped videos in table                                  │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Load videos from database after scraping                           │
│  - [ ] Populate CTkTable with video data                                 │
│  - [ ] Add columns: title, channel, views, date                           │
│  - [ ] Add clickable thumbnail URLs (open in browser)                    │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/ui/main_window.py                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### PHASE 2: BASIC INTELLIGENCE (P1)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P1-1: GEMINI AI INTEGRATION (SUB-NICHE SUGGESTIONS)                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 4 hours                                                          │
│  Dependencies: P0-ALL                                                      │
│  Output: Get 5 sub-niche suggestions from category                         │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Setup Gemini AI API key                                            │
│  - [ ] Implement classify_sub_niches_simple()                            │
│  - [ ] Use 100 video titles as input (for MVP)                            │
│  - [ ] Display 5 sub-niches as radio buttons                              │
│  - [ ] User selects 1 sub-niche                                          │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/api/gemini_client.py                                          │
│  - hunterbot/modules/classifier.py                                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P1-2: FOCUSED SCRAPING (ROUND 2)                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 2 hours                                                          │
│  Dependencies: P1-1, P0-5                                                  │
│  Output: Scrape 100 videos for selected sub-niche                          │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Modify Hunter to accept sub-niche query                           │
│  - [ ] Scrape new batch of videos                                         │
│  - [ ] Save to separate table or add round_number field                    │
│                                                                             │
│  MVP Limitation: 100 videos per round                                     │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/modules/hunter.py                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P1-3: BASIC FILTERING                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 2 hours                                                          │
│  Dependencies: P1-2                                                        │
│  Output: Filter videos by views threshold                                  │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Add filter by views (min 50k)                                     │
│  - [ ] Add filter by subscriber count (max 30k)                           │
│  - [ ] Sort by views (descending)                                         │
│  - [ ] Display top 10 in results table                                    │
│                                                                             │
│  Note: No ML yet, just rule-based filtering                             │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/modules/analyst.py                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P1-4: TRANSCRIPT FETCHING (YT-DLP FALLBACK)                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 4 hours                                                          │
│  Dependencies: P1-2                                                        │
│  Output: Get transcripts for top 10 videos                                 │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Install yt-dlp                                                     │
│  - [ ] Implement ytdlp_extract_transcript()                              │
│  - [ ] Save to database (transcript_raw field)                            │
│  - [ ] Handle missing transcripts gracefully                             │
│                                                                             │
│  MVP Limitation: No Deepgram API, only auto-captions                    │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/modules/hunter.py                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### PHASE 3: FULL FEATURES (P2)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P2-1: DEEPGRAM API INTEGRATION                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 4 hours                                                          │
│  Dependencies: P1-ALL                                                      │
│  Output: High-quality transcripts using Deepgram                           │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Setup Deepgram API key                                             │
│  - [ ] Implement audio download (yt-dlp + ffmpeg)                        │
│  - [ ] Implement Deepgram transcription                                   │
│  - [ ] Fallback to yt-dlp if Deepgram fails                             │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/api/deepgram_client.py                                        │
│  - hunterbot/modules/hunter.py                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P2-2: DATA SANITIZER                                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 3 hours                                                          │
│  Dependencies: P2-1                                                        │
│  Output: Clean transcripts with quality scoring                            │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Implement remove_filler_words()                                  │
│  - [ ] Implement remove_timestamps()                                     │
│  - [ ] Implement quality_scoring()                                       │
│  - [ ] Update video state to CLEANED/FAILED                              │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/modules/sanitizer.py                                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P2-3: TIER 1 VALIDATION                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 3 hours                                                          │
│  Dependencies: P2-2                                                        │
│  Output: Filter videos by Tier 1 audience signals                         │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Implement language detection (langdetect)                          │
│  - [ ] Implement currency detection                                       │
│  - [ ] Calculate tier1_confidence_score                                  │
│  - [ ] Filter by threshold (70%)                                          │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/modules/geo_validator.py                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P2-4: ML PIPELINE (ISOLATION FOREST + DBSCAN)                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 6 hours                                                          │
│  Dependencies: P2-3                                                        │
│  Output: Top 10 viral outliers using ML                                    │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Implement feature_engineering()                                   │
│  - [ ] Implement hard_filter() (subs, views, age)                       │
│  - [ ] Implement isolation_forest_filter()                              │
│  - [ ] Implement dbscan_refinement()                                    │
│  - [ ] Calculate composite_score                                          │
│  - [ ] Select top 10 outliers                                            │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/modules/analyst.py                                            │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P2-5: AI CONTENT GENERATION                                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 5 hours                                                          │
│  Dependencies: P2-4                                                        │
│  Output: Generate EDSA scripts, titles, SEO for top 10                    │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Implement generate_titles()                                       │
│  - [ ] Implement generate_edsa_script()                                   │
│  - [ ] Implement generate_seo_description()                              │
│  - [ ] Implement generate_thumbnail_prompt()                             │
│  - [ ] Save to database (state='READY')                                   │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/modules/architect.py                                         │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ TASK P2-6: EXCEL EXPORT                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  Effort: 3 hours                                                          │
│  Dependencies: P2-5                                                        │
│  Output: Export top 10 to Excel file                                     │
│                                                                             │
│  Tasks:                                                                    │
│  - [ ] Implement export_to_excel()                                       │
│  - [ ] Create 3 sheets (Summary, Content, Competitor)                     │
│  - [ ] Add formatting (headers, colors)                                   │
│  - [ ] Save file with timestamp                                           │
│                                                                             │
│  Files:                                                                    │
│  - hunterbot/modules/exporter.py                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## EFFORT ESTIMATION

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TOTAL EFFORT BY PHASE                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PHASE 1 (Foundation)  P0:  16 hours (2 days)                            │
│  PHASE 2 (Basic AI)     P1:  16 hours (2 days)                            │
│  PHASE 3 (Full Features) P2:  21 hours (3 days)                            │
│                                                                             │
│  MVP TOTAL (P0):        16 hours                                          │
│  FULL PRODUCT:         53 hours (~1 week)                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## MVP FEATURE CHECKLIST

### MVP (P0) - Must Have for First Release

```
DATABASE:
- [ ] SQLite database created
- [ ] videos table with minimal columns
- [ ] Can insert and query video records

UI:
- [ ] Category input field
- [ ] Start button
- [ ] Progress bar/label
- [ ] Results table
- [ ] Basic error messages

SCRAPING:
- [ ] YouTube API connection working
- [ ] Search by query works
- [ ] Fetches metadata (title, views, channel, etc.)
- [ ] Saves to database
- [ ] Updates UI with progress

WORKFLOW:
- [ ] User enters category
- [ ] Clicks start
- [ ] Progress shows "Scraping: 1/100, 2/100..."
- [ ] Results displayed in table
- [ ] No crashes on errors
```

---

## POST-MVP ROADMAP

```
v1.0 (MVP):
- Category → Scrape 100 videos → Display results
- No AI, no ML, no transcripts

v1.1:
- Add Gemini AI (sub-niche suggestions)
- Add Round 2 scraping (focused)
- Add basic filtering (views threshold)

v1.2:
- Add transcript fetching (yt-dlp)
- Add data sanitizer
- Add tier1 validation

v1.3:
- Add Deepgram API
- Add ML pipeline (Isolation Forest + DBSCAN)
- Add content generation

v1.4:
- Add Excel export
- Add setup wizard
- Add logging

v2.0:
- Full production-ready application
- All features from PRD v2.1.1
```

---

## DEVELOPMENT ORDER (STEP-BY-STEP)

### Week 1: MVP Foundation

```
Day 1-2:
  - P0-1: Project skeleton
  - P0-2: Database setup
  - Test: Database creates successfully

Day 3:
  - P0-3: Basic UI framework
  - Test: Window opens, button clickable

Day 4:
  - P0-4: YouTube API integration
  - Test: Can fetch 10 videos

Day 5:
  - P0-5: Scraping orchestration
  - P0-6: UI results display
  - Test: Full workflow works

MVP COMPLETE: Working scraper with UI
```

---

## GETTING STARTED CHECKLIST

Before coding Phase 1:

```
ENVIRONMENT:
- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] YouTube Data API key obtained
- [ ] Git repository initialized

ACCOUNTS:
- [ ] Google Cloud Project created
- [ ] YouTube Data API v3 enabled
- [ ] API key generated

RECOMMENDED START:
1. Start with P0-1 (project skeleton)
2. Test each task before moving to next
3. Commit after each P0 task completion
```

---

*For detailed specifications, see PRD_PHASE_1 files*
