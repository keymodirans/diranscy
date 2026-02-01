# 09 ERROR HANDLING

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

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

