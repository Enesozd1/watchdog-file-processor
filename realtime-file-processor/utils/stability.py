import time
from pathlib import Path


def wait_until_stable(
    path: Path,
    check_interval: float = 0.2,
    stable_checks: int = 3,
    timeout: float = 10.0,
) -> bool:
    """
    Returns True if file becomes stable, False if timeout or file disappears.
    """
    start = time.time()
    last_size = -1
    same_count = 0

    while time.time() - start < timeout:
        if not path.exists():
            return False

        try:
            size = path.stat().st_size
        except OSError:
            return False

        if size == last_size:
            same_count += 1
            if same_count >= stable_checks:
                return True
        else:
            same_count = 0
            last_size = size

        time.sleep(check_interval)

    return False