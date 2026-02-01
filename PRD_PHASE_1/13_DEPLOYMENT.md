# 13 DEPLOYMENT

**PRD Version:** 2.1.1
**Last Updated:** February 1, 2026
**Related:** [Index](00_INDEX.md)

---

## 16. DEPLOYMENT GUIDE

### Nuitka Compilation

**Why Nuitka:**

- Compile Python to native executable (.exe)
- No Python installation required on user machine
- Faster startup than PyInstaller
- Better performance (C-level compilation)

**Build Script:**

```python
# build.py

import subprocess
import os
import sys

def build_executable():
    """
    Compile Hunterbot to Windows .exe using Nuitka.
    
    Requirements:
    - Nuitka installed: pip install nuitka
    - MSVC (Microsoft Visual C++) compiler installed
    - ffmpeg.exe in project directory (for bundling)
    """
    
    print("Building Hunterbot.exe with Nuitka...")
    
    command = [
        sys.executable, '-m', 'nuitka',
        '--standalone',                         # Include all dependencies
        '--onefile',                            # Single executable file
        '--windows-disable-console',            # No console window (GUI app)
        '--enable-plugin=tk-inter',             # Support CustomTkinter
        '--include-data-dir=assets=assets',     # Bundle assets folder
        '--include-data-file=ffmpeg.exe=ffmpeg.exe',  # Bundle ffmpeg
        '--include-package=sklearn',            # Include scikit-learn
        '--include-package=pandas',             # Include pandas
        '--include-package=deepgram',           # Include Deepgram SDK
        '--include-package=google',             # Include Google APIs
        '--output-dir=dist',                    # Output directory
        '--output-filename=Hunterbot.exe',      # Executable name
        '--company-name=Hunterbot',
        '--product-name=Hunterbot',
        '--file-version=2.0.0',
        '--product-version=2.0.0',
        '--file-description=YouTube Reverse Engineering Bot',
        'hunterbot/main.py'                     # Entry point
    ]
    
    print(f"Command: {' '.join(command)}\n")
    
    result = subprocess.run(command)
    
    if result.returncode == 0:
        print("\n" + "="*60)
        print("BUILD SUCCESSFUL!")
        print("="*60)
        print(f"Executable: dist/Hunterbot.exe")
        print(f"Size: ~{os.path.getsize('dist/Hunterbot.exe') // 1024 // 1024} MB")
    else:
        print("\n" + "="*60)
        print("BUILD FAILED!")
        print("="*60)
        sys.exit(1)

if __name__ == '__main__':
    build_executable()
```

**Run Build:**

```bash
python build.py
```

**Expected Output:**

- `dist/Hunterbot.exe` (single file, ~80-120MB)
- No external dependencies required (all bundled)

---

### First-Run Setup Wizard

**On first launch, guide user through API key setup:**

```python
# hunterbot/ui/setup_wizard.py

import customtkinter as ctk

class SetupWizard:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Hunterbot - First Time Setup")
        self.window.geometry("600x500")
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create setup UI."""
        title = ctk.CTkLabel(
            self.window,
            text="Welcome to Hunterbot!",
            font=("Segoe UI", 20, "bold")
        )
        title.pack(pady=20)
        
        subtitle = ctk.CTkLabel(
            self.window,
            text="Let's set up your API keys to get started.",
            font=("Segoe UI", 12)
        )
        subtitle.pack(pady=10)
        
        # YouTube API Keys Section
        youtube_frame = ctk.CTkFrame(self.window)
        youtube_frame.pack(pady=20, padx=20, fill="both")
        
        ctk.CTkLabel(
            youtube_frame,
            text="YouTube Data API Keys",
            font=("Segoe UI", 14, "bold")
        ).pack(pady=10)
        
        self.youtube_entries = []
        for i in range(5):
            entry = ctk.CTkEntry(
                youtube_frame,
                placeholder_text=f"YouTube API Key {i+1}",
                width=400
            )
            entry.pack(pady=5)
            self.youtube_entries.append(entry)
        
        # Similar sections for Deepgram and Gemini
        
        # Save button
        save_btn = ctk.CTkButton(
            self.window,
            text="Save & Start",
            command=self.save_keys,
            height=45
        )
        save_btn.pack(pady=20)
    
    def save_keys(self):
        """Save API keys to database."""
        # Validate keys (test with API call)
        # Save to api_keys table
        # Close wizard, launch main app
        pass
    
    def run(self):
        self.window.mainloop()
```


---

### File Structure (Complete)

```
hunterbot/
├── hunterbot/
│   ├── __init__.py
│   ├── main.py                  # Entry point
│   ├── config.py                # Config management
│   ├── database/
│   │   ├── __init__.py
│   │   ├── schema.py            # SQL schema
│   │   └── models.py            # ORM models
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── classifier.py
│   │   ├── hunter.py
│   │   ├── sanitizer.py
│   │   ├── geo_validator.py
│   │   ├── analyst.py
│   │   ├── architect.py
│   │   ├── exporter.py
│   │   └── guardian.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── controller.py
│   │   ├── setup_wizard.py
│   │   └── screens/
│   │       ├── __init__.py
│   │       ├── step1_category.py
│   │       ├── step2_scraping.py
│   │       ├── step3_transcript.py
│   │       ├── step4_filtering.py
│   │       ├── step5_generation.py
│   │       └── step6_export.py
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       ├── logger.py
│       └── helpers.py
├── assets/
│   └── icons/
│       ├── check-circle-green.png
│       ├── alert-triangle-orange.png
│       ├── x-circle-red.png
│       ├── info-blue.png
│       ├── loader-blue.gif
│       ├── key-grey.png
│       ├── database-grey.png
│       └── file-spreadsheet-green.png
├── tests/
│   ├── __init__.py
│   ├── test_hunter.py
│   ├── test_sanitizer.py
│   ├── test_analyst.py
│   └── fixtures/
│       └── videos_sample.csv
├── exports/                     # Excel output directory
├── requirements.txt
├── build.py                     # Nuitka build script
├── setup_dependencies.bat       # Dependency installer
├── .env.example                 # API key template
└── README.md
```


---

