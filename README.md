# HUNTERBOT MVP

## VERSION

Version: 1.0.0-mvp
Status: Development

---

## DESKRIPSI

Hunterbot MVP adalah aplikasi desktop Windows untuk scraping video YouTube berdasarkan kategori/keyword.

## FITUR MVP

1. Input kategori/keyword
2. Scraping 100 video metadata dari YouTube
3. Tampilkan hasil di tabel
4. Simpan ke database SQLite

## PERSYARATAN

### System

- Python 3.11+
- Windows 10/11

### API Keys

- YouTube Data API v3 key (WAJIB)

### Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Setup environment variables (salin .env.example ke .env)
cp .env.example .env

# Edit .env dan masukkan YouTube API key
```

---

## CARA RUN

```bash
# Pastikan environment variable sudah diset
set YOUTUBE_API_KEY=your_api_key

# Atau buat file .env
# Windows (PowerShell):
# $env:YOUTUBE_API_KEY = "your_api_key"

# Jalankan aplikasi
python hunterbot/main.py
```

---

## STRUKTUR PROJECT

```
hunterbot/
├── __init__.py
├── main.py                     # Entry point
├── config.py                   # Konfigurasi global
├── database/
│   ├── __init__.py
│   ├── schema.py                 # SQL schema
│   └── models.py                 # Video model
├── modules/
│   ├── __init__.py
│   └── hunter.py                 # Scraping module
├── api/
│   ├── __init__.py
│   └── youtube_api.py            # YouTube API client
├── ui/
│   ├── __init__.py
│   └── main_window.py             # UI utama
├── utils/
│   ├── __init__.py
│   └── logger.py                 # Logging system
├── logs/                          # Log files (auto-created)
├── exports/                       # Output files (auto-created)
└── hunterbot.db                   # Database (auto-created)

```

---

## CLEAN ARCHITECTURE

### Layers

```
PRESENTATION (ui/)
└── UI components, event handlers

BUSINESS LOGIC (modules/)
└── Scraping logic, orchestration

DATA LAYER (database/)
└── Database operations, models

EXTERNAL APIS (api/)
└── Third-party API integrations

UTILITIES (utils/)
└── Logging, helpers
```

---

## LOGGING

Semua log menggunakan Bahasa Indonesia untuk kemudahan debugging.

Log file dibuat otomatis di folder `logs/` dengan format:
- `hunterbot_YYYYMMDD.log`

Level log yang digunakan:
- DEBUG: Detail info untuk development
- INFO: Info normal (progress, berhasil)
- PERINGATAN: Warning yang perlu perhatian
- ERROR: Error yang terjadi
- KRITIS: Critical error yang stop aplikasi

---

## DEVELOPMENT NOTES

- Gunakan absolute imports: `from hunterbot.module import X`
- Type hints untuk semua function
- Docstrings untuk semua class dan method
- Error handling dengan try-except
- Logging untuk semua operasi penting

---

## TESTING

```bash
# Run tests (belum ada test di MVP)
pytest

# Run manual test
python hunterbot/main.py
```

---

## NEXT STEPS (POST-MVP)

1. Tambah Gemini AI untuk sub-niche suggestions
2. Tambah Round 2 scraping (focused ke sub-niche)
3. Tambah transcript fetching (yt-dlp)
4. Tambah Deepgram API untuk transcript
5. Tambah ML Pipeline (Isolation Forest + DBSCAN)
6. Tambah Excel Export

---

*Untuk detail lengkap, lihat PRD_PHASE_1 folder*
