import time
from pathlib import Path
from typing import Optional
import location

def get_oldest_root_desktop_file(days: int = 3) -> Optional[Path]:
    """
    Scan only the files directly on the Windows Desktop (no subfolders)
    and return the oldest file older than `days`. Returns None if none found.
    """
    desktop = Path.home() / "Desktop/RIP"
    if not desktop.exists():
        raise FileNotFoundError(f"Desktop not found at {desktop}")

    cutoff = time.time() - days * 86400
    oldest_file = None
    oldest_mtime = float('inf')

    for entry in desktop.iterdir():
        if entry.is_file():
            try:
                mtime = entry.stat().st_mtime
            except OSError as e:
                print(f"Warning: can't stat '{entry}': {e}")
                continue

            if mtime < cutoff and mtime < oldest_mtime:
                oldest_mtime = mtime
                oldest_file = entry
                
    if oldest_file:
        location.open_folder_containing_file(desktop)
        
    return oldest_file

