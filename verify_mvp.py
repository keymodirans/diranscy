"""
Quick test script untuk verifikasi struktur Hunterbot MVP.

File ini untuk test import dan struktur tanpa perlu API key.
"""

def test_config():
    """Test config module."""
    from hunterbot import config
    print(f"Database path: {config.Config.DATABASE_PATH}")
    print(f"Logs dir: {config.LOGS_DIR}")
    print(f"Exports dir: {config.EXPORTS_DIR}")
    return True


def test_database():
    """Test database module."""
    from hunterbot.database import schema
    conn = schema.init_database()
    cursor = conn.execute('PRAGMA database_list')
    result = cursor.fetchone()
    print(f"Database created at: {result[0] if result else 'unknown'}")
    conn.close()
    return True


def test_models():
    """Test models module."""
    from hunterbot.database.models import Video
    print("Video model imported successfully")
    return True


def test_youtube_api():
    """Test YouTube API client import."""
    from hunterbot.api.youtube_api import YouTubeAPI
    print("YouTube API client imported successfully")
    return True


def test_modules():
    """Test modules."""
    from hunterbot.modules.hunter import HunterModule
    print("Hunter module imported successfully")
    return True


def test_ui():
    """Test UI module."""
    try:
        import customtkinter as ctk
        print("CustomTkinter available:", ctk.__version__)
        from hunterbot.ui.main_window import HunterbotWindow
        print("UI module imported successfully (window class defined)")
        return True
    except ImportError as e:
        print(f"CustomTkinter belum terinstall: {e}")
        return False


def main():
    """Jalankan semua test."""
    print("=" * 50)
    print("HUNTERBOT MVP - VERIFICATION TEST")
    print("=" * 50)
    print()

    tests = [
        ("Config", test_config),
        ("Database Schema", test_database),
        ("Models", test_models),
        ("YouTube API", test_youtube_api),
        ("Modules", test_modules),
        ("UI", test_ui),
    ]

    results = []
    for name, test_func in tests:
        try:
            test_func()
            results.append((name, "PASS"))
            print(f"[PASS] {name}")
        except Exception as e:
            results.append((name, "FAIL"))
            print(f"[FAIL] {name}: {e}")

    print()
    print("=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    for name, status in results:
        print(f"  {name}: {status}")

    passed = sum(1 for _, status in results if status == "PASS")
    total = len(results)

    print()
    print(f"Hasil: {passed}/{total} tests passed")

    if passed == total:
        print()
        print("SEMUA MODULE SIAP! Aplikasi siap digunakan.")
        print("Jalankan dengan: py -m hunterbot.main.py")
    else:
        print()
        print("ADA MODULE GAGAL. Cek error di atas.")


if __name__ == "__main__":
    main()
