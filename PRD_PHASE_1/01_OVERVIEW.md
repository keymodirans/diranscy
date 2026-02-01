# 01 OVERVIEW

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

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

