"""
Main Window untuk Hunterbot MVP.

UI utama aplikasi Hunterbot menggunakan CustomTkinter.
"""

import tkinter as tk
from tkinter import messagebox
import threading
import logging
from datetime import datetime
import queue

import customtkinter as ctk
from typing import Optional, List, Dict, Any

from hunterbot.config import Config
from hunterbot.modules.hunter import HunterModule
from hunterbot.database.models import Video
from hunterbot.utils.logger import setup_logging, get_logger

# Inisialisasi logging
setup_logging()
logger = get_logger(__name__)


# UPDATED: Custom LogHandler untuk mengirim log ke UI
class UILogHandler(logging.Handler):
    """
    LogHandler yang mengirim log message ke UI via queue.

    Thread-safe untuk digunakan di background thread.
    """

    def __init__(self, log_queue: queue.Queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record: logging.LogRecord) -> None:
        """
        Kirim log record ke queue.

        Args:
            record: LogRecord dari logger.
        """
        try:
            # Format pesan log
            timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
            level = record.levelname[:4]  # INFO, WARN, ERROR, etc
            message = self.format(record)

            # Kirim ke queue
            log_entry = f"[{timestamp}] [{level}] {message}"
            self.log_queue.put(log_entry)

        except Exception:
            # Self.handleError() biar gak crash logging
            self.handleError(record)


class HunterbotWindow(ctk.CTk):
    """
    Main window aplikasi Hunterbot.

    Window ini menyediakan UI sederhana untuk:
    - Input category/keyword
    - Start scraping
    - Lihat progress
    - Tampilkan hasil
    """

    def __init__(self):
        """Inisialisasi main window."""
        super().__init__()

        self.title(Config.WINDOW_TITLE)
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")

        # Variables
        self.category_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Siap untuk scraping")
        self.progress_var = tk.DoubleVar(value=0.0)
        self.videos_data: List[Dict[str, Any]] = []

        # UPDATED: Setup log queue untuk UI
        self.log_queue = queue.Queue()
        self._setup_ui_logging()

        # Inisialisasi UI
        self._create_widgets()

        # UPDATED: Start log polling untuk update UI
        self._poll_logs()

        # Center window
        self.center_window()

        logger.info("Main window dibuat")

    def _setup_ui_logging(self) -> None:
        """
        Setup logging handler untuk mengirim log ke UI.
        """
        # Buat UI log handler
        self.ui_log_handler = UILogHandler(self.log_queue)
        self.ui_log_handler.setLevel(logging.INFO)  # Hanya INFO ke atas

        # Format: simple tanpa timestamp karena kita tambah manual
        formatter = logging.Formatter("%(message)s")
        self.ui_log_handler.setFormatter(formatter)

        # Add ke root logger (atau specific logger yang mau dimonitor)
        # Monitor semua log dari hunterbot modules
        for logger_name in ["hunterbot.modules.hunter", "hunterbot.api.youtube_api",
                           "hunterbot.modules.geo_validator", "hunterbot.database.models"]:
            log = logging.getLogger(logger_name)
            log.addHandler(self.ui_log_handler)

    def _poll_logs(self) -> None:
        """
        Poll log queue dan update UI log viewer.

        Dipanggil setiap 100ms via after().
        """
        try:
            # Proses semua logs yang ada di queue
            while not self.log_queue.empty():
                log_entry = self.log_queue.get_nowait()
                self._append_log(log_entry)

        except queue.Empty:
            pass

        # Schedule next poll
        self.after(100, self._poll_logs)

    def _append_log(self, log_entry: str) -> None:
        """
        Append log entry ke log viewer widget.

        Thread-safe dari _poll_logs (main thread).

        Args:
            log_entry: Formatted log message.
        """
        if hasattr(self, "log_viewer"):
            # Insert log di end
            self.log_viewer.insert("end", log_entry + "\n")

            # Scroll otomatis ke bawah
            self.log_viewer.see("end")

            # Optional: limit max lines (biar gak makan memory)
            # self.log_viewer.delete("1.0", "100.0")  # Keep only last 900 lines

    def _create_widgets(self) -> None:
        """Buat semua widget UI."""
        # UPDATED: Reorganize layout - logs di bawah status bar
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header - fixed
        self.grid_rowconfigure(1, weight=0)  # Input - fixed
        self.grid_rowconfigure(2, weight=1)  # Results - expandable
        self.grid_rowconfigure(3, weight=0)  # Status - fixed
        self.grid_rowconfigure(4, weight=0)  # Logs - fixed height

        # Header
        self._create_header()

        # Input Section
        self._create_input_section()

        # Results Section (expandable)
        self._create_results_section()

        # Status Bar
        self._create_status_bar()

        # UPDATED: Logs Section (di bawah status bar)
        self._create_logs_section()

    def _create_header(self) -> None:
        """Buat header frame."""
        header_frame = ctk.CTkFrame(self, height=80)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        header_frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            header_frame,
            text="HUNTERBOT",
            font=("Segoe UI", 24, "bold")
        )
        title_label.pack(side="top", pady=(10, 5))

        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="YouTube Viral Video Discovery - MVP Version",
            font=("Segoe UI", 12)
        )
        subtitle_label.pack(side="top")

    def _create_input_section(self) -> None:
        """Buat section input category."""
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        input_frame.grid_columnconfigure(1, weight=1)

        # Label
        label = ctk.CTkLabel(
            input_frame,
            text="Kategori / Keyword:",
            font=("Segoe UI", 12)
        )
        label.grid(row=0, column=0, padx=(0, 10), pady=10)

        # Entry
        entry = ctk.CTkEntry(
            input_frame,
            textvariable=self.category_var,
            placeholder_text="Contoh: Horror, History Documentary, Gaming",
            width=400
        )
        entry.grid(row=0, column=1, padx=(0, 10), pady=10)

        # Button
        button = ctk.CTkButton(
            input_frame,
            text="Mulai Scraping",
            command=self.start_scraping,
            width=120
        )
        button.grid(row=0, column=2, pady=10)

    def _create_results_section(self) -> None:
        """
        Buat section hasil scraping (expandable).

        UPDATED: Results table saja, tanpa split.
        """
        results_frame = ctk.CTkFrame(self)
        results_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        results_frame.grid_rowconfigure(1, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

        # Label untuk tabel
        label = ctk.CTkLabel(
            results_frame,
            text="Hasil Scraping",
            font=("Segoe UI", 12, "bold")
        )
        label.pack(side="top", pady=(10, 5))

        # Text widget untuk hasil (MVP: simple text)
        self.results_text = ctk.CTkTextbox(
            results_frame,
            font=("Consolas", 10)
        )
        self.results_text.pack(
            side="top",
            fill="both",
            expand=True,
            padx=(10, 10),
            pady=(0, 10)
        )

    def _create_logs_section(self) -> None:
        """
        Buat section progress logs (fixed height).

        UPDATED: Logs di bawah status bar.
        """
        # Container frame untuk logs dengan fixed height
        logs_container = ctk.CTkFrame(self)
        logs_container.grid(row=4, column=0, sticky="nsew", padx=20, pady=(0, 10))
        logs_container.grid_rowconfigure(0, weight=1)
        logs_container.grid_columnconfigure(0, weight=1)
        logs_container.grid_columnconfigure(1, weight=0)

        # Logs header dengan tombol reset
        logs_header_frame = ctk.CTkFrame(logs_container)
        logs_header_frame.grid(row=0, column=0, sticky="ew", padx=(5, 5), pady=(5, 5))
        logs_header_frame.grid_columnconfigure(0, weight=1)
        logs_header_frame.grid_columnconfigure(1, weight=0)

        # Logs label
        logs_label = ctk.CTkLabel(
            logs_header_frame,
            text="Progress Logs",
            font=("Segoe UI", 10, "bold")
        )
        logs_label.grid(row=0, column=0, sticky="w", padx=(10, 5))

        # UPDATED: Tombol reset logs
        reset_logs_btn = ctk.CTkButton(
            logs_header_frame,
            text="Reset Logs",
            command=self._reset_logs,
            width=80,
            height=24
        )
        reset_logs_btn.grid(row=0, column=1, padx=(5, 10), pady=(0, 0))

        # Logs viewer textbox
        self.log_viewer = ctk.CTkTextbox(
            logs_container,
            font=("Consolas", 9),
            activate_scrollbars=True,
            height=150  # Fixed height
        )
        self.log_viewer.grid(row=0, column=0, sticky="nsew", padx=(5, 5), pady=(0, 5))

        # Initial log message
        self.log_viewer.insert("1.0", "=== Log Progress ===\n")
        self.log_viewer.insert("end", "Siap untuk scraping...\n\n")

    def _create_status_bar(self) -> None:
        """Buat status bar."""
        status_frame = ctk.CTkFrame(self, height=40)
        status_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        status_frame.grid_columnconfigure(0, weight=1)

        # Status label
        status_label = ctk.CTkLabel(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 10),
            anchor="w"
        )
        status_label.grid(row=0, column=0, sticky="w", padx=10)

    def center_window(self) -> None:
        """Pusatkan window di layar."""
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - Config.WINDOW_WIDTH) // 2
        y = (screen_height - Config.WINDOW_HEIGHT) // 2
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}+{x}+{y}")

    def start_scraping(self) -> None:
        """Handler untuk tombol mulai scraping."""
        query = self.category_var.get().strip()

        if not query:
            messagebox.showwarning("Input Kosong", "Silakan masukkan kategori atau keyword")
            return

        # UPDATED: Clear logs sebelum scraping baru
        if hasattr(self, "log_viewer"):
            self.log_viewer.delete("1.0", "end")
            self.log_viewer.insert("1.0", f"=== Memulai Scraping: {query} ===\n\n")

        # Clear results
        if hasattr(self, "results_text"):
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", "Sedang scraping...\n")

        logger.info(f"User memulai scraping: query='{query}'")

        # Update status
        self.status_var.set("Memulai scraping...")

        # Run scraping di background thread
        thread = threading.Thread(target=self._run_scraping, args=(query,))
        thread.daemon = True
        thread.start()

    def _run_scraping(self, query: str) -> None:
        """
        Jalankan proses scraping (di background thread).

        Args:
            query: Query pencarian.
        """
        try:
            # Buat hunter module instance
            hunter = HunterModule()

            # Set callback progress
            hunter.set_progress_callback(self._update_progress)

            # Jalankan scraping dengan target 100 videos (sesuai MVP)
            stats = hunter.scrape_videos(query, target_count=100)

            # Tampilkan hasil
            self._display_results()

            passed_count = stats.get("passed_all", 0)
            total_scraped = stats.get("total_scraped", 0)

            self.status_var.set(
                f"Selesai! {passed_count}/{total_scraped} video lulus filter"
            )

        except Exception as e:
            logger.error(f"Scraping gagal: {e}")
            self.status_var.set(f"Gagal: {str(e)}")
            messagebox.showerror("Error", f"Gagal scraping: {str(e)}")

    def _update_progress(self, current: int, total: int) -> None:
        """
        Update progress bar dan status.

        Args:
            current: Nomor saat ini.
            total: Total target.
        """
        progress = current / total if total > 0 else 0
        self.progress_var.set(progress)

        if total > 0:
            percentage = int(progress * 100)
            self.status_var.set(f"Scraping: {current}/{total} ({percentage}%)")
        else:
            self.status_var.set(f"Scraping: {current} video...")

    def _reset_logs(self) -> None:
        """
        Reset log viewer untuk kosongkan logs.

        Dipanggil saat tombol "Reset Logs" diklik.
        """
        if hasattr(self, "log_viewer"):
            self.log_viewer.delete("1.0", "end")
            self.log_viewer.insert("1.0", "=== Log Progress ===\n")
            self.log_viewer.insert("end", "Logs telah di-reset. Siap untuk logging baru.\n\n")
            logger.info("Log viewer di-reset oleh user")

    def _display_results(self) -> None:
        """Tampilkan hasil scraping ke text widget."""
        videos = Video.get_all(limit=100)  # UPDATED: Tampilkan sampai 100 video

        if not videos:
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", "Tidak ada video yang ditemukan.")
            return

        # Bersihkan text widget
        self.results_text.delete("1.0", "end")

        # Header dengan 9 kolom
        header = (
            f"{'NO.':<4} {'NEGARA':<12} {'TANGGAL':<12} {'WAKTU':<8} {'UMUR':<6} "
            f"{'TAYANGAN':>12} {'SUBSCRIBER':>12} {'VPH':>10} {'ER%':>8} {'CHANNEL':<25}\n"
        )
        self.results_text.insert("end", header)
        self.results_text.insert("end", "-" * 130 + "\n")

        # Data rows
        for idx, video in enumerate(videos, 1):
            country = video.country_name[:10] if video.country_name else "Unknown"
            date_only = video.upload_date_only
            time_only = video.upload_time_only
            age = f"{video.upload_days_ago}h" if video.upload_days_ago else "0h"
            views = video.views_formatted
            subs = video.subscribers_formatted
            vph = f"{video.vph:.0f}" if video.vph > 0 else "0"
            er = f"{video.engagement_rate:.1f}" if video.engagement_rate > 0 else "0.0"
            channel_short = video.channel_title[:22] + "..." if len(video.channel_title) > 22 else video.channel_title

            row = (
                f"{idx:<4} {country:<12} {date_only:<12} {time_only:<8} {age:<6} "
                f"{views:>12} {subs:>12} {vph:>10} {er:>8} {channel_short:<25}\n"
            )
            self.results_text.insert("end", row)

        # Footer
        footer = f"\nTotal: {len(videos)} video ditampilkan"
        self.results_text.insert("end", footer)
