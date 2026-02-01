# 08 DATA FLOW STATE

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

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

