import time
from pathlib import Path


def wait_until_stable(
    path: Path,
    conf,
    
) -> bool:
    """
    Returns True if file becomes stable, False if timeout or file disappears.
    """
    check_interval = conf["check_interval"]
    stable_checks = conf["stable_checks"]
    timeout = conf["timeout"]
    
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