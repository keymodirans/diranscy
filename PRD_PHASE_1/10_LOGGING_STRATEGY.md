# 10 LOGGING STRATEGY

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

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

