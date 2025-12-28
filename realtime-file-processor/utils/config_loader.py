import json
from pathlib import Path
from typing import Any, Dict


class IncompleteJson(Exception):
    pass



REQUIRED_KEYS = [
    "watch_path",
    "processed_path",
    "dry_run",
    "log_file",
    "log_level",
    
]


def load_config(config_path: Path) -> Dict[str, Any]:
    with config_path.open("r", encoding="utf-8") as f:
        conf = json.load(f)

    for key in REQUIRED_KEYS:
        if key not in conf:
            raise IncompleteJson(f"Missing config key: {key}")
    
    # (Optional but helpful) normalize extensions
    # ensures [".txt"] not ["txt"]
    

    return conf
