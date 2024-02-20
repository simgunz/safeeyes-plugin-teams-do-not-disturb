import logging
import os
import platform
from pathlib import Path

SKIP_BREAKS_STATUSES = ["presenting", "on-the-phone"]


def on_pre_break(break_obj) -> bool:
    """Lifecycle method executes before the pre-break period."""
    return _should_skip_break()


def on_start_break(break_obj) -> bool:
    """Lifecycle method executes just before the break."""
    return _should_skip_break()


def _user_data_dir() -> Path:
    """Get user data directory."""
    system = platform.system()
    if system == "Windows":
        # Typically, C:\Users\<User>\AppData\Local
        data_dir = Path(os.getenv("LOCALAPPDATA"))
    elif system == "Darwin":
        # Typically, /Users/<User>/Library/Application Support
        data_dir = Path.home() / "Library" / "Application Support"
    else:  # Linux and other Unix-like systems
        # XDG standard for Linux; fallback to HOME if not set
        data_dir = Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return data_dir


def _should_skip_break() -> bool:
    safeeyes_presence_file = _user_data_dir() / "safeeyes" / "teamspresence"
    presence = safeeyes_presence_file.read_text()
    if presence in SKIP_BREAKS_STATUSES:
        logging.info(f"Teams presence status is {presence}. Skipping break.")
        return True
    return False
