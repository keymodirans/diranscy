# 14 CODE GENERATION

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

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

