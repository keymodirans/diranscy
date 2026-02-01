# 15 APPENDIX

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

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

