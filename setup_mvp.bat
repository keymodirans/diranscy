@echo off
echo ========================================
echo HUNTERBOT MVP - SETUP & VERIFY
echo ========================================
echo.

echo [1/5] Checking Python installation...
py -3.11 --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python 3.11 tidak ditemukan!
    echo.
    echo Silakan install Python 3.11+ dulu dari:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
) else (
    echo Python ditemukan: OK
)

echo.
echo [2/5] Installing dependencies...
cd "%~dp0"
py -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Ada dependency yang gagal install, tapi lanjut verifikasi...
)

echo.
echo [3/5] Checking file structure...
dir /b hunterbot\*.py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Folder structure tidak sesuai!
    pause
    exit /b 1
)
echo Found Python files: %ERRORLEVEL% files

echo.
echo [4/5] Verifying Python syntax...
echo Testing imports...

py -c "import sys; sys.path.insert(0, 'hunterbot')"
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Import check gagal!
    pause
    exit /b 1
)

echo.
echo Testing module imports...
py -c "from hunterbot import config" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] hunterbot.config
) else (
    echo [PASS] hunterbot.config
)

py -c "from hunterbot.database import schema" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] hunterbot.database.schema
) else (
    echo [PASS] hunterbot.database.schema
)

py -c "from hunterbot.database import models" 2>nul
if %ERRORLEVEL% NEQ 0 then (
    echo [FAIL] hunterbot.database.models
) else (
    echo [PASS] hunterbot.database.models
)

py -c "from hunterbot.utils import logger" 2>nul
if %ERRORLEVEL% NEQ 0; then
    echo [FAIL] hunterbot.utils.logger
) else (
    echo [PASS] hunterbot.utils.logger
)

py -c "from hunterbot.api import youtube_api" 2>nul
if %ERRORLEVEL% NEQ 0; then
    echo [FAIL] hunterbot.api.youtube_api
) else (
    echo [PASS] hunterbot.api.youtube_api
)

py -c "from hunterbot.modules import hunter" 2>nul
if %ERRORLEVEL% NEQ 0; then
    echo [FAIL] hunterbot.modules.hunter
) else (
    echo [PASS] hunterbot.modules.hunter
)

echo.
echo [5/5] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo File .env dibuat dari .env.example
    echo.
    echo PENTING: Edit file .env dan masukkan YouTube API Key kamu!
    echo   YOUTUBE_API_KEY=your_api_key_here
    echo.
)

echo.
echo ========================================
echo VERIFICATION SELESAI
echo ========================================
echo.
echo Sekarang setup:
echo   1. Edit file .env dan masukkan: YOUTUBE_API_KEY=key_anda
echo   2. Jalankan: py -m hunterbot.main.py
echo.
echo File yang dibuat:
dir /b hunterbot\*.py
dir /b hunterbot\database\*.py
dir /b hunterbot\api\*.py
dir /b hunterbot\ui\*.py
dir /b hunterbot\utils\*.py

echo.
pause
