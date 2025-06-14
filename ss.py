import os
import time
from pathlib import Path
from typing import List

def get_old_desktop_files(days: int = 3) -> List[Path]:
    """
    Scan the user's Desktop on Windows and return a list of file paths
    last modified more than `days` days ago.

    :param days: number of days ago threshold
    :return: list of Path objects
    """
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        raise FileNotFoundError(f"Desktop folder not found at {desktop}")

    cutoff = time.time() - days * 86400  # 86400 seconds in a day

    old_files = []
    for entry in desktop.rglob('*'):
        if entry.is_file():
            try:
                mtime = entry.stat().st_mtime
            except OSError as e:
                # Could be a permissions issue or broken symlink
                print(f"Warning: Could not stat {entry!r}: {e}")
                continue

            if mtime < cutoff:
                old_files.append(entry)

    return old_files
