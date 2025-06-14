import subprocess
import sys
from typing import Optional

def shutdown_windows(delay_seconds: int = 0, force: bool = False, comment: Optional[str] = None) -> None:
    """
    Shutdown a Windows PC.

    :param delay_seconds: Delay before shutdown in seconds (default 0 for immediate).
    :param force: If True, forcibly close running applications.
    :param comment: Optional message displayed on shutdown dialog.
    :raises RuntimeError: If shutdown command fails.
    """
    args = ["shutdown", "/s", f"/t", str(delay_seconds)]
    if force:
        args.append("/f")
    if comment:
        args.extend(["/c", comment])

    try:
        result = subprocess.run(args, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(f"Shutdown command failed: {exc.stderr.strip() or exc}") from exc


shutdown_windows()
