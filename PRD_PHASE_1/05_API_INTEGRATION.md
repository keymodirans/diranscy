# 05 API INTEGRATION

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

---

## 7. API INTEGRATION

### 7.1 YouTube Data API v3

**Official Documentation:** https://developers.google.com/youtube/v3/docs

**Authentication:**

- Method: API Key (query parameter `key`)
- Obtain key: Google Cloud Console > APIs \& Services > Credentials
- Quota: 10,000 units per day per project
- Quota reset: Daily at midnight Pacific Time

**Quota Costs:**


| Operation | Endpoint | Cost (units) |
| :-- | :-- | :-- |
| Search videos | `search.list` | 100 |
| Get video details | `videos.list` | 1 |
| Get channel details | `channels.list` | 1 |

**Strategy:** Use 5 API keys = 50,000 units/day capacity (enough for 5 full runs)

#### Endpoint 1: search.list (Video Discovery)

**Purpose:** Search YouTube videos by keyword, filter by region and language.

**Implementation:**

```python
import requests
from typing import List, Tuple, Optional

def youtube_search(
    api_key: str,
    query: str,
    max_results: int = 50,
    published_after: Optional[str] = None,
    region_code: str = 'US',
    page_token: Optional[str] = None
) -> Tuple[List[str], Optional[str]]:
    """
    Search YouTube videos with Tier 1 geo-targeting.
    
    Args:
        api_key: YouTube Data API key
        query: Search keyword (sub-niche name)
        max_results: Results per page (max 50)
        published_after: ISO 8601 date (e.g., "2025-01-01T00:00:00Z")
        region_code: Target country code ("US" for Tier 1)
        page_token: Pagination token from previous response
    
    Returns:
        Tuple of (video_ids: list, next_page_token: str or None)
    
    Raises:
        QuotaExceededException: If API quota exhausted
        InvalidAPIKeyException: If API key is invalid
    """
    url = 'https://www.googleapis.com/youtube/v3/search'
    
    params = {
        'key': api_key,
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'order': 'viewCount',  # Sort by views (descending)
        'maxResults': max_results,
        'regionCode': region_code,  # Tier 1 targeting
        'relevanceLanguage': 'en',  # English content only
        'videoDefinition': 'any',  # Include all quality levels
        'videoEmbeddable': 'true',  # Only embeddable videos
    }
    
    if published_after:
        params['publishedAfter'] = published_after
    
    if page_token:
        params['pageToken'] = page_token
    
    response = requests.get(url, params=params, timeout=30)
    
    # Error handling
    if response.status_code != 200:
        handle_youtube_api_error(response)
    
    data = response.json()
    
    # Extract video IDs
    video_ids = [item['id']['videoId'] for item in data.get('items', [])]
    next_page_token = data.get('nextPageToken')
    
    return video_ids, next_page_token


def handle_youtube_api_error(response: requests.Response):
    """Handle YouTube API errors with specific exceptions."""
    if response.status_code == 403:
        error_data = response.json()
        error_reason = error_data['error']['errors']['reason']
        
        if error_reason == 'quotaExceeded':
            raise QuotaExceededException("YouTube API quota exceeded for this key")
        elif error_reason == 'forbidden':
            raise InvalidAPIKeyException("YouTube API key is invalid or restricted")
    
    elif response.status_code == 404:
        raise VideoNotFoundException("Requested video not found")
    
    elif response.status_code >= 500:
        raise YouTubeServerException(f"YouTube API server error: {response.status_code}")
    
    else:
        raise Exception(f"YouTube API error {response.status_code}: {response.text}")


# Custom exceptions
class QuotaExceededException(Exception):
    pass

class InvalidAPIKeyException(Exception):
    pass

class VideoNotFoundException(Exception):
    pass

class YouTubeServerException(Exception):
    pass
```


#### Endpoint 2: videos.list (Detailed Metadata)

**Purpose:** Get detailed metadata for videos (batch operation, up to 50 IDs).

**Implementation:**

```python
def youtube_videos_details(api_key: str, video_ids: List[str]) -> List[dict]:
    """
    Get detailed metadata for videos (batch).
    
    Args:
        api_key: YouTube Data API key
        video_ids: List of video IDs (max 50)
    
    Returns:
        List of video metadata dictionaries
    
    Quota Cost: 1 unit (regardless of number of IDs up to 50)
    """
    if len(video_ids) > 50:
        raise ValueError("Maximum 50 video IDs per request")
    
    url = 'https://www.googleapis.com/youtube/v3/videos'
    
    params = {
        'key': api_key,
        'part': 'snippet,statistics,contentDetails',
        'id': ','.join(video_ids)
    }
    
    response = requests.get(url, params=params, timeout=30)
    
    if response.status_code != 200:
        handle_youtube_api_error(response)
    
    data = response.json()
    videos = []
    
    for item in data.get('items', []):
        video = {
            'video_id': item['id'],
            'title': item['snippet']['title'],
            'description': item['snippet']['description'],
            'channel_id': item['snippet']['channelId'],
            'channel_title': item['snippet']['channelTitle'],
            'upload_date': item['snippet']['publishedAt'],
            'duration': item['contentDetails']['duration'],
            'category_id': item['snippet'].get('categoryId'),
            'views': int(item['statistics'].get('viewCount', 0)),
            'likes': int(item['statistics'].get('likeCount', 0)),
            'comments': int(item['statistics'].get('commentCount', 0)),
            'tags': item['snippet'].get('tags', []),  # UPDATED: Add tags for SEO/analysis
            'thumbnails': item['snippet']['thumbnails']
        }
        videos.append(video)
    
    return videos
```


#### Endpoint 3: channels.list (Channel Subscriber Count)

**Purpose:** Get channel subscriber count for V-Score calculation.

**Implementation:**

```python
def youtube_channel_subscribers(api_key: str, channel_id: str) -> int:
    """
    Get channel subscriber count.
    
    Args:
        api_key: YouTube Data API key
        channel_id: YouTube channel ID
    
    Returns:
        Subscriber count (integer)
    
    Quota Cost: 1 unit
    """
    url = 'https://www.googleapis.com/youtube/v3/channels'
    
    params = {
        'key': api_key,
        'part': 'statistics',
        'id': channel_id
    }
    
    response = requests.get(url, params=params, timeout=30)
    
    if response.status_code != 200:
        handle_youtube_api_error(response)
    
    data = response.json()
    
    if data.get('items'):
        stats = data['items']['statistics']
        return int(stats.get('subscriberCount', 0))
    
    return 0
```


#### Thumbnail Extraction (From API Response)

**Purpose:** Get highest quality thumbnail URL available.

**Implementation:**

```python
def extract_thumbnail(thumbnails_dict: dict) -> dict:
    """
    Extract best available thumbnail from API response.
    
    Args:
        thumbnails_dict: thumbnails object from YouTube API
    
    Returns:
        dict: {
            'url': str,
            'width': int,
            'height': int,
            'quality': str
        }
    
    Priority: maxres > standard > high > medium > default
    """
    quality_order = ['maxres', 'standard', 'high', 'medium', 'default']
    
    for quality in quality_order:
        if quality in thumbnails_dict:
            thumb = thumbnails_dict[quality]
            return {
                'url': thumb['url'],
                'width': thumb.get('width'),
                'height': thumb.get('height'),
                'quality': quality
            }
    
    # Fallback (should never happen)
    return {
        'url': f'https://i.ytimg.com/vi/default.jpg',
        'width': 120,
        'height': 90,
        'quality': 'default'
    }
```


---

### 7.2 Deepgram API

**Official Documentation:** https://developers.deepgram.com/docs

**Authentication:**

- Method: Bearer token (HTTP header: `Authorization: Token YOUR_KEY`)
- Obtain key: Deepgram Console > API Keys
- Pricing: ~\$0.0125 per minute
- Free tier: \$200 credit (~12,000 minutes)

**Model:** nova-2 (latest as of Feb 2026, best accuracy for English)

#### Implementation

```python
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
import subprocess
import os
from typing import Optional

def deepgram_transcribe(video_url: str, api_key: str) -> str:
    """
    Transcribe YouTube video audio using Deepgram.
    
    Process:
    1. Download audio with yt-dlp (requires ffmpeg)
    2. Send to Deepgram API
    3. Extract transcript text
    4. Clean up temporary files
    
    Args:
        video_url: YouTube video URL
        api_key: Deepgram API key
    
    Returns:
        Transcript text (string)
    
    Raises:
        FileNotFoundError: If ffmpeg not installed
        DeepgramException: If transcription fails
    """
    # Step 1: Download audio
    audio_file = download_audio_ytdlp(video_url)
    
    try:
        # Step 2: Initialize Deepgram client
        deepgram = DeepgramClient(api_key)
        
        # Step 3: Read audio file
        with open(audio_file, 'rb') as audio:
            buffer_data = audio.read()
        
        payload: FileSource = {
            'buffer': buffer_data
        }
        
        # Step 4: Configure transcription options
        options = PrerecordedOptions(
            model='nova-2',  # Latest model (Feb 2026)
            language='en',
            punctuate=True,  # Add punctuation
            diarize=False,  # No speaker identification (not needed for faceless content)
            smart_format=True,  # Format dates, times, numbers
            utterances=False,  # Don't split by speaker
            paragraphs=False  # Return as continuous text
        )
        
        # Step 5: Transcribe
        response = deepgram.listen.rest.v('1').transcribe_file(payload, options)
        
        # Step 6: Extract transcript text
        transcript = response['results']['channels']['alternatives']['transcript']
        
        return transcript
    
    finally:
        # Step 7: Cleanup temporary audio file
        if os.path.exists(audio_file):
            os.remove(audio_file)


def download_audio_ytdlp(video_url: str) -> str:
    """
    Download audio from YouTube using yt-dlp.
    
    Args:
        video_url: YouTube video URL
    
    Returns:
        Path to downloaded audio file (.mp3)
    
    Raises:
        FileNotFoundError: If yt-dlp or ffmpeg not installed
        subprocess.CalledProcessError: If download fails
    
    Requirements:
        - yt-dlp installed: pip install yt-dlp
        - ffmpeg installed: choco install ffmpeg (Windows)
    """
    # Extract video ID for filename
    video_id = video_url.split('=')[-1].split('&')
    output_file = f'temp_audio_{video_id}.mp3'
    
    command = [
        'yt-dlp',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--audio-quality', '0',  # Best quality
        '--output', output_file,
        '--no-playlist',
        video_url
    ]
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300,  # 5 minute timeout
            check=True
        )
        
        if not os.path.exists(output_file):
            raise FileNotFoundError(f"yt-dlp failed to create audio file: {output_file}")
        
        return output_file
    
    except subprocess.TimeoutExpired:
        raise Exception(f"Audio download timeout after 5 minutes: {video_url}")
    
    except subprocess.CalledProcessError as e:
        if 'ffmpeg' in e.stderr.lower():
            raise FileNotFoundError(
                "ffmpeg not found. Install with: choco install ffmpeg"
            )
        raise Exception(f"yt-dlp download failed: {e.stderr}")


def ytdlp_extract_transcript_fallback(video_url: str) -> Optional[str]:
    """
    Fallback: Extract transcript using yt-dlp (YouTube auto-captions).
    
    This is FREE but less accurate than Deepgram.
    Use only when Deepgram quota exhausted or API fails.
    
    Args:
        video_url: YouTube video URL
    
    Returns:
        Transcript text or None if unavailable
    """
    video_id = video_url.split('=')[-1].split('&')
    transcript_file = f'temp_transcript_{video_id}.en.vtt'
    
    command = [
        'yt-dlp',
        '--skip-download',
        '--write-auto-sub',
        '--sub-lang', 'en',
        '--sub-format', 'vtt',
        '--output', f'temp_transcript_{video_id}',
        video_url
    ]
    
    try:
        subprocess.run(command, capture_output=True, text=True, check=True, timeout=60)
        
        if os.path.exists(transcript_file):
            with open(transcript_file, 'r', encoding='utf-8') as f:
                vtt_content = f.read()
            
            # Clean VTT format (remove timestamps, tags)
            transcript = clean_vtt_format(vtt_content)
            
            # Cleanup
            os.remove(transcript_file)
            
            return transcript
    
    except:
        pass
    
    return None


def clean_vtt_format(vtt_text: str) -> str:
    """Remove VTT formatting (timestamps, tags)."""
    import re
    
    # Remove WEBVTT header
    text = re.sub(r'WEBVTT.*?\n\n', '', vtt_text, flags=re.DOTALL)
    
    # Remove timestamps (00:00:00.000 --> 00:00:05.000)
    text = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}\.\d{3}', '', text)
    
    # Remove position/alignment tags
    text = re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)
    text = re.sub(r'align:start position:\d+%', '', text)
    
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Remove multiple newlines
    text = re.sub(r'\n{2,}', '\n', text)
    
    return text.strip()
```


---

### 7.3 Gemini AI

**Official Documentation:** https://ai.google.dev/docs

**Authentication:**

- Method: API Key (SDK handles header automatically)
- Obtain key: Google AI Studio > Get API Key
- Model: `gemini-1.5-pro` (128K context window, multimodal)
- Pricing: Free tier 60 requests/minute


#### Implementation

```python
import google.generativeai as genai
import json
import html
from typing import List, Dict
from tenacity import retry, stop_after_attempt, wait_exponential

class GeminiClient:
    def __init__(self, api_key: str, config: dict):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(config['gemini']['model'])
        self.config = config
        self.banned_terms = config['gemini']['banned_terms']
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def classify_sub_niches_from_transcripts(
        self,
        category: str,
        transcripts: List[str],
        titles: List[str]
    ) -> Dict:
        """
        Classify 1000 transcripts into 5 specific sub-niches (Round 1).

        Args:
            category: Broad niche (e.g., "Horror")
            transcripts: 1000 cleaned video transcripts
            titles: 1000 video titles (for reference)

        Returns:
            dict: {
                'category': str,
                'sub_niches': [
                    {
                        'name': str,
                        'video_count': int,
                        'demand': 'High' | 'Medium' | 'Low',
                        'examples': [str, str, str]
                    },
                    ...
                ]
            }
        """
        safe_category = html.escape(category)

        # Prepare transcript snippets (first 200 words each for context)
        transcript_snippets = []
        for i, (title, transcript) in enumerate(zip(titles, transcripts)):
            safe_title = html.escape(title[:100])
            safe_transcript = html.escape(transcript[:200])  # First 200 words
            transcript_snippets.append(f"VIDEO {i+1}: {safe_title}\n{safe_transcript}")

        all_snippets = '\n\n---\n\n'.join(transcript_snippets[:1000])

        prompt = f"""<task>
You are a YouTube content analyst. Analyze these 1000 video transcripts from the category "{safe_category}" and identify the top 5 most dominant sub-niches (specific topic clusters).

ANALYSIS METHOD:
1. Read ALL transcript snippets to understand content themes
2. Cluster videos by similar topics/angles/approaches
3. Identify 5 distinct sub-niches with highest demand

For each sub-niche, provide:
1. Sub-niche name (2-4 words, specific, searchable keywords)
2. Video count (how many videos belong to this sub-niche)
3. Demand score (High if count > 200, Medium if 100-200, Low if < 100)
4. Example titles (3 representative video titles)

RULES:
- Sub-niches must be SPECIFIC (not broad)
- Focus on HIGH DEMAND topics (most videos cluster here)
- No overlap between sub-niches
- Sub-niche names should be YouTube search keywords
- Analyze FULL transcript content, not just titles

TRANSCRIPT SAMPLES (First 200 words each):
{all_snippets}

Output (JSON only, no markdown):
{{
  "category": "{safe_category}",
  "sub_niches": [
    {{"name": "...", "video_count": N, "demand": "High/Medium/Low", "examples": ["...", "...", "..."]}},
    ...
  ]
}}
</task>"""

        response = self.model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 2000
            }
        )

        # Parse JSON response
        try:
            result = json.loads(response.text)
            return result
        except json.JSONDecodeError:
            raise Exception("Gemini returned invalid JSON")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def classify_sub_niches(self, category: str, sample_titles: List[str]) -> Dict:
        """
        DEPRECATED: Use classify_sub_niches_from_transcripts() instead.
        This method is kept for backward compatibility.
        """
        pass
Output (JSON only, no markdown):
{{
  "category": "{safe_category}",
  "sub_niches": [
    {{"name": "...", "video_count": N, "demand": "High/Medium/Low", "examples": ["...", "...", "..."]}},
    ...
  ]
}}
</task>"""
        
        response = self.model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'max_output_tokens': 1000
            }
        )
        
        # Parse JSON response
        try:
            result = json.loads(response.text)
            return result
        except json.JSONDecodeError:
            # Retry will be handled by @retry decorator
            raise Exception("Gemini returned invalid JSON")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def generate_titles(self, video_title: str, transcript_preview: str) -> List[str]:
        """
        Generate 3 click-magnet title variations.
        
        Args:
            video_title: Original competitor title
            transcript_preview: First 500 words of transcript
        
        Returns:
            List of 3 title variations
        """
        safe_title = html.escape(video_title)
        safe_transcript = html.escape(transcript_preview[:500])
        
        prompt = f"""<task>
You are a YouTube viral title specialist. Generate 3 click-magnet title variations for a faceless educational video.

Input Video Title (Competitor):
"{safe_title}"

Transcript Preview (First 500 words):
{safe_transcript}

Generate 3 title variations that:
1. Use psychological triggers (curiosity gap, shock, urgency)
2. Keep under 60 characters (mobile-friendly)
3. Include power words (Secret, Untold, Revealed, Hidden, Truth)
4. Avoid clickbait red flags (ALL CAPS, excessive punctuation)
5. Stay true to content (no misleading claims)

Output format (JSON):
{{
  "titles": [
    "Title variation 1",
    "Title variation 2",
    "Title variation 3"
  ]
}}
</task>

<examples>
Original: "The History of World War 2"
Generated:
1. "The Untold Secret That Changed WW2 Forever"
2. "What They Never Taught You About World War 2"
3. "The Hidden Truth Behind WW2's Biggest Mystery"
</examples>

<constraints>
- No banned terms: "subscribe", "like", "click", "comment", "bell icon"
- No exaggeration (avoid "INSANE", "SHOCKING" overuse)
- Factual accuracy (verifiable claims only)
</constraints>"""
        
        response = self.model.generate_content(
            prompt,
            generation_config={'temperature': 0.7, 'max_output_tokens': 200}
        )
        
        try:
            result = json.loads(response.text)
            return result['titles']
        except:
            # Fallback if JSON parsing fails
            return [video_title] * 3
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def generate_edsa_script(
        self,
        video_title: str,
        transcript_cleaned: str,
        chapters: List[Dict],
        duration_seconds: int
    ) -> str:
        """
        Generate EDSA script from competitor transcript.
        
        Args:
            video_title: Competitor title
            transcript_cleaned: Cleaned transcript (full)
            chapters: List of chapter dicts
            duration_seconds: Video duration
        
        Returns:
            EDSA script (string, 2000-5000 words)
        
        Raises:
            BannedTermsException: If script contains banned terms after 3 retries
        """
        safe_title = html.escape(video_title)
        safe_transcript = html.escape(transcript_cleaned)
        
        # Format chapters
        chapters_text = ""
        if chapters and len(chapters) > 0:
            chapters_text = "Chapter Breakdown:\n" + "\n".join([
                f"- {ch['timestamp']} {html.escape(ch['title'])}"
                for ch in chapters[:5]
            ])
        
        prompt = f"""<task>
Rewrite this competitor YouTube transcript into a NEW original EDSA script for faceless content.

EDSA Framework:
- E = Engage (Hook: First 5-10 seconds, open loop)
- D = Deliver (Main content: Educational value, storytelling)
- S = Sustain (Retention tactics: Mini-cliffhangers, callbacks)
- A = Amplify (Conclusion: Emotional peak, key takeaway)

Input Data:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Original Title: "{safe_title}"
Duration: {duration_seconds} seconds
{chapters_text}

Competitor Transcript (Cleaned):
{safe_transcript}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your Task:
1. HOOK (0-10 sec): Create urgent open loop (teaser, shocking fact, mystery)
2. STRUCTURE: Mimic competitor's chapter flow (intro, 3-5 sections, conclusion)
3. RETENTION: Add mini-hooks every 60-90 seconds ("But here's where it gets interesting...")
4. STORYTELLING: Transform facts into narrative (characters, conflict, resolution)
5. ORIGINALITY: Different words, same structure (avoid plagiarism)
6. LENGTH: Target {duration_seconds * 150} words (~150 words per minute voiceover)

Output: Full EDSA script (plain text, no markdown formatting)
</task>

<banned_terms>
DO NOT include these phrases (YouTube spam policy):
- "Subscribe to my channel"
- "Like this video"
- "Hit the bell icon"
- "Check the description"
- "Link in description below"
- "Comment below"
- "Smash that like button"
- "Don't forget to subscribe"
</banned_terms>

<example_hook>
BAD: "Hello everyone, today we're talking about World War 2..."
GOOD: "One decision in 1944 killed 50,000 soldiers in 24 hours. The generals knew it would fail. They sent them anyway. Here's why."
</example_hook>"""
        
        response = self.model.generate_content(
            prompt,
            generation_config={'temperature': 0.7, 'max_output_tokens': 8000}
        )
        
        script = response.text
        
        # Validate banned terms
        if not self._validate_banned_terms(script):
            raise BannedTermsException("Script contains banned terms")
        
        return script
    
    def _validate_banned_terms(self, text: str) -> bool:
        """Check if text contains banned terms."""
        text_lower = text.lower()
        for term in self.banned_terms:
            if term.lower() in text_lower:
                return False
        return True
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def generate_seo_description(
        self,
        title: str,
        script_preview: str
    ) -> Dict:
        """
        Generate SEO description and keywords.
        
        Args:
            title: Selected title (from title_options)
            script_preview: First 1000 words of EDSA script
        
        Returns:
            dict: {
                'description': str (150-200 words),
                'keywords': list (10 keywords)
            }
        """
        safe_title = html.escape(title)
        safe_script = html.escape(script_preview[:1000])
        
        prompt = f"""<task>
Generate YouTube video description optimized for search ranking.

Input:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Video Title: "{safe_title}"
Script Preview (First 1000 words):
{safe_script}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generate:
1. Description (150-200 words):
   - First 2-3 sentences: Hook + video summary
   - Middle: Key points covered (bullet points)
   - End: Call to curiosity (not subscribe CTA)

2. Keywords (10 keywords):
   - Mix of broad + long-tail keywords
   - Relevant to video content
   - High search volume potential

Output format (JSON):
{{
  "description": "Full description text...",
  "keywords": ["keyword1", "keyword2", ..., "keyword10"]
}}
</task>"""
        
        response = self.model.generate_content(
            prompt,
            generation_config={'temperature': 0.7, 'max_output_tokens': 500}
        )
        
        try:
            return json.loads(response.text)
        except:
            return {
                'description': f"Watch this video about {title}",
                'keywords': [title.lower()]
            }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=8),
        reraise=True
    )
    def generate_thumbnail_prompt(self, title: str, thumbnail_url: str) -> str:
        """
        Generate thumbnail description for AI image generation.
        
        Args:
            title: Video title
            thumbnail_url: Competitor thumbnail URL (for reference)
        
        Returns:
            Text prompt for Midjourney/DALL-E
        """
        safe_title = html.escape(title)
        
        prompt = f"""<task>
Create a detailed prompt for AI image generation (Midjourney/DALL-E) to create a YouTube thumbnail.

Video Title: "{safe_title}"
Competitor Thumbnail: {thumbnail_url} (for style reference)

Describe visual elements for thumbnail that:
1. HIGH CONTRAST: Bold colors, clear focal point
2. CURIOSITY GAP: Visual teaser (mysterious object, dramatic scene)
3. TEXT OVERLAY: 3-5 words max (large, readable font)
4. EMOTIONAL TRIGGER: Shock, awe, intrigue
5. MINIMALIST: One main subject, simple background

Output format (plain text description for Midjourney/DALL-E):
Describe foreground, background, color scheme, text overlay, composition.
</task>

<example_output>
"Foreground: Close-up of a rusted World War 2 tank barrel pointing directly at camera, dramatic angle. Background: Blurred smoke and fire, dark grey tones with orange highlights. Color scheme: Desaturated war tones (grey, brown, orange fire glow). Text overlay: Large bold white text 'THE SECRET WEAPON' with slight shadow for readability, positioned top-right. Composition: Rule of thirds, tank barrel occupies left 2/3 of frame, text balances right side. Lighting: Cinematic rim lighting on tank metal, high contrast shadows. Mood: Intense, mysterious, historical drama. Style: Photorealistic documentary thumbnail."
</example_output>"""
        
        response = self.model.generate_content(
            prompt,
            generation_config={'temperature': 0.7, 'max_output_tokens': 300}
        )
        
        return response.text


class BannedTermsException(Exception):
    pass
```


---

