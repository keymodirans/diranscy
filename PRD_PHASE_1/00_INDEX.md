# HUNTERBOT - PRD PHASE 1 INDEX

**Version:** 2.1.1
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
| 2.1 | 2026-02-01 | User corrections (tags, hard filters) | The Sentinel Architect |
| 2.1.1 | 2026-02-01 | 2-Round architecture implementation | The Sentinel Architect |

### Changelog Summary

**v2.0 CRITICAL FIXES:**
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
15. Updated hard filter: added views <= subscriber_count x 50 (anti-paid promotion)
16. Updated YouTube API integration to include tags in metadata extraction
17. Updated examples with tags field included

**v2.1.1 UPDATES (2-Round Architecture):**
18. Changed from 1-round to 2-round scraping architecture
19. Round 1: Exploratory scraping (1000 videos) -> Clustering -> 5 sub-niches
20. Round 2: Focused scraping (1000 NEW videos) -> ML filtering -> Content generation
21. Updated Classifier module to use 1000 transcripts instead of 100 titles
22. Updated Hunter module to run twice (category -> sub-niche)
23. Added GeminiClient.classify_sub_niches_from_transcripts() method
24. Updated total videos processed: 1000 -> 2000 per session
25. Updated processing time: 50-70 min -> 100-140 min
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

This PRD is split into 16 topic-based files for better readability and maintenance.

| File | Description | Lines (Approx) |
|------|-------------|---------------|
| **00_INDEX.md** | This file - Navigation and quick reference | - |
| **01_OVERVIEW.md** | Executive Summary, Product Vision, Target Users | ~200 |
| **02_ARCHITECTURE.md** | System Architecture, Tech Stack, Dependencies | ~300 |
| **03_DATABASE_SCHEMA.md** | Complete Database Design, Tables, Indexes | ~500 |
| **04_MODULE_SPECS.md** | 8 Core Module Specifications | ~1500 |
| **05_API_INTEGRATION.md** | YouTube, Deepgram, Gemini APIs | ~1200 |
| **06_ML_PIPELINE.md** | Machine Learning Pipeline, Feature Engineering | ~400 |
| **07_UI_DESIGN.md** | User Interface, Screens, Icons | ~600 |
| **08_DATA_FLOW_STATE.md** | State Machine, Transitions, Rollback | ~500 |
| **09_ERROR_HANDLING.md** | Retry Logic, Always/Ask/Never Boundaries | ~400 |
| **10_LOGGING_STRATEGY.md** | Logging Levels, Rotation, Export | ~300 |
| **11_SECURITY_PERFORMANCE.md** | Security Best Practices, Optimization | ~400 |
| **12_TESTING_STRATEGY.md** | Unit Tests, Integration Tests | ~400 |
| **13_DEPLOYMENT.md** | Nuitka Build, Setup Wizard, File Structure | ~500 |
| **14_CODE_GENERATION.md** | Instructions for AI Code Generation | ~300 |
| **15_APPENDIX.md** | Decision Log, References | ~200 |
| **16_CHANGELOG.md** | Detailed Version History | ~200 |

**Total Lines:** ~7,000 lines across 17 files

---

## QUICK NAVIGATION

### For Developers
- Start here: **01_OVERVIEW.md** - Understand what we're building
- Then: **02_ARCHITECTURE.md** - High-level system design
- Then: **03_DATABASE_SCHEMA.md** - Data model
- Then: **04_MODULE_SPECS.md** - Implementation details

### For AI Code Generation
- Read: **14_CODE_GENERATION.md** first
- Then: **04_MODULE_SPECS.md** for module-by-module implementation
- Reference: **05_API_INTEGRATION.md** for external API calls

### For QA/Testing
- Start: **12_TESTING_STRATEGY.md**
- Reference: **09_ERROR_HANDLING.md** for edge cases

### For Deployment
- Read: **13_DEPLOYMENT.md** - Build and setup instructions
- Reference: **02_ARCHITECTURE.md** - Tech stack requirements

---

## PROJECT AT A GLANCE

```
Product: Hunterbot
Platform: Windows Desktop (v1.0)
Language: Python 3.11+
GUI: CustomTkinter
Database: SQLite
ML: scikit-learn (Isolation Forest + DBSCAN)
AI: Gemini 1.5 Pro

Architecture: 2-Round Scraping
- Round 1: 1000 videos -> Sub-niche discovery
- Round 2: 1000 videos -> ML filtering -> Content generation

Processing Time: 100-140 minutes per session
Output: 10 production-ready content packages (Excel)
```

---

## DOCUMENT STRUCTURE CONVENTIONS

All PRD files follow this structure:
1. Section headers use `##` (H2)
2. Subsections use `###` (H3)
3. Code blocks use ` ``` ` with language specified
4. Tables use Markdown format
5. No emoji or icons (clean documentation)
6. Line max 100 characters

---

*For detailed information, refer to individual topic files listed above.*
