import os
import time
from pathlib import Path
from typing import Optional

def get_oldest_old_desktop_file(days: int = 3) -> Optional[Path]:
    """
    Scan the Windows Desktop and return the oldest file modified 
    more than `days` days ago. Returns None if no such file exists.
    """
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        raise FileNotFoundError(f"Desktop not found at {desktop}")

    cutoff = time.time() - days * 86400  # days ago in seconds
    oldest_file = None
    oldest_mtime = float('inf')

    for path in desktop.rglob('*'):
        if path.is_file():
            try:
                mtime = path.stat().st_mtime
            except OSError as e:
                print(f"Warning: cannot access '{path}': {e}")
                continue

            if mtime < cutoff and mtime < oldest_mtime:
                oldest_mtime = mtime
                oldest_file = path

    return oldest_file

