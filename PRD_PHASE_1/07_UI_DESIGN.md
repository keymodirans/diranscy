# 07 UI DESIGN

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

---

## 10. USER INTERFACE DESIGN

### Design System

**Color Palette:**

```python
# Light Mode (Default)
COLOR_BACKGROUND = "#FCFCF9"
COLOR_SURFACE = "#FFFFFE"
COLOR_TEXT = "#13343B"
COLOR_TEXT_SECONDARY = "#626C71"
COLOR_PRIMARY = "#21808D"
COLOR_PRIMARY_HOVER = "#1D7480"
COLOR_SUCCESS = "#21808D"
COLOR_ERROR = "#C0152F"
COLOR_WARNING = "#A84B2F"
COLOR_BORDER = "rgba(94,82,64,0.2)"

# Dark Mode (Auto-detect system theme)
COLOR_BACKGROUND_DARK = "#1F2121"
COLOR_SURFACE_DARK = "#262828"
COLOR_TEXT_DARK = "#F5F5F5"
COLOR_PRIMARY_DARK = "#32B8C6"
```

**Typography:**

```python
FONT_FAMILY = "Segoe UI"
FONT_SIZE_TITLE = 18
FONT_SIZE_SECTION = 14
FONT_SIZE_LABEL = 11
FONT_SIZE_INPUT = 12
FONT_SIZE_BUTTON = 12
FONT_SIZE_LOG = 10
```

**Layout Constants:**

```python
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
PADDING = 20
PADDING_SMALL = 10
INPUT_HEIGHT = 40
BUTTON_HEIGHT = 45
PROGRESS_BAR_HEIGHT = 25
LOG_BOX_HEIGHT = 180
```


---

### Screen Flow (7 Steps)

**Step 1: Category \& Sub-Niche Selection**

```
Category Input Field
    ↓
[ANALISIS SUB-NICHE Button]
    ↓
5 Radio Buttons (sub-niche options)
    ↓
Target Video Count Dropdown
    ↓
[LANJUT KE SCRAPING Button]
```

**Step 2-7:** Progress screens with real-time logging

---

### Lucide Icons (Embedded PNG Files)

**Complete Icon List:**


| Icon File | Size | Color | Use Case |
| :-- | :-- | :-- | :-- |
| `check-circle-green.png` | 20x20 | \#32A852 | Success indicators |
| `alert-triangle-orange.png` | 20x20 | \#FFA500 | Warning messages |
| `x-circle-red.png` | 20x20 | \#E74C3C | Error messages |
| `info-blue.png` | 20x20 | \#3498DB | Info messages |
| `loader-blue.gif` | 20x20 | \#3498DB (animated) | Processing state |
| `key-grey.png` | 20x20 | \#9D9D9D | API key status |
| `database-grey.png` | 20x20 | \#9D9D9D | Database operations |
| `file-spreadsheet-green.png` | 24x24 | \#32A852 | Export success |

**Loading Icons:**

```python
from PIL import Image
import customtkinter as ctk

def load_icon(filename: str) -> ctk.CTkImage:
    """Load icon from assets/icons/ directory."""
    image = Image.open(f"assets/icons/{filename}")
    return ctk.CTkImage(light_image=image, dark_image=image, size=(20, 20))

# Load all icons at startup
ICONS = {
    "check": load_icon("check-circle-green.png"),
    "warning": load_icon("alert-triangle-orange.png"),
    "error": load_icon("x-circle-red.png"),
    "info": load_icon("info-blue.png"),
    "loader": load_icon("loader-blue.gif"),
    "key": load_icon("key-grey.png"),
    "database": load_icon("database-grey.png"),
    "export": load_icon("file-spreadsheet-green.png")
}
```

**Fallback Strategy:**

```python
def load_icon_with_fallback(filename: str) -> ctk.CTkImage:
    """Load icon with fallback to placeholder if file missing."""
    try:
        image = Image.open(f"assets/icons/{filename}")
        return ctk.CTkImage(light_image=image, dark_image=image, size=(20, 20))
    except FileNotFoundError:
        # Create placeholder (solid color square)
        placeholder = Image.new('RGB', (20, 20), color='#626C71')
        return ctk.CTkImage(light_image=placeholder, dark_image=placeholder, size=(20, 20))
```


---

