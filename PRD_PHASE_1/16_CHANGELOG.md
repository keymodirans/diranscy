# 16 CHANGELOG

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

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

