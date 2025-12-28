from pathlib import Path
import logging

EXTENSION_MAP = {
    #Images
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".bmp": "Images",
    ".gif": "Images",
    ".tiff": "Images",
    ".webp": "Images",
    ".svg": "Images",
    ".ico": "Images",

    #Documents
    ".pdf": "Documents",
    ".txt": "Documents",
    ".doc": "Documents",
    ".docx": "Documents",
    ".odt": "Documents",
    ".rtf": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".csv": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",

    #Code / Data
    ".cpp": "Code",
    ".py": "Code",
    ".js": "Code",
    ".ts": "Code",
    ".html": "Code",
    ".css": "Code",
    ".json": "Code",
    ".xml": "Code",
    ".yaml": "Code",
    ".yml": "Code",
    ".sql": "Code",
    ".md": "Code",
    ".c": "Code",
    ".h": "Code",
    ".hpp": "Code",
    ".cs": "Code",
    ".java": "Code",
    ".kt": "Code",
    ".kts": "Code",
    ".swift": "Code",
    ".go": "Code",
    ".rs": "Code",
    ".rb": "Code",
    ".php": "Code",
    ".scala": "Code",
    ".groovy": "Code",
    ".lua": "Code",
    ".r": "Code",
    ".jl": "Code",
    ".dart": "Code",
    ".asm": "Code",
    ".s": "Code",
    ".ps1": "Code",
    ".bat": "Code",
    ".cmd": "Code",
    ".sh": "Code",
    ".zsh": "Code",
    ".fish": "Code",

    #Audio
    ".mp3": "Audio",
    ".wav": "Audio",
    ".flac": "Audio",
    ".aac": "Audio",
    ".ogg": "Audio",
    ".m4a": "Audio",

    #Video
    ".mp4": "Video",
    ".mkv": "Video",
    ".avi": "Video",
    ".mov": "Video",
    ".wmv": "Video",
    ".flv": "Video",
    ".webm": "Video",

    #Archives
    ".zip": "Archives",
    ".rar": "Archives",
    ".7z": "Archives",
    ".tar": "Archives",
    ".gz": "Archives",
    ".bz2": "Archives",
    ".xz": "Archives",

    #Disk images / installers
    ".iso": "Installers",
    ".exe": "Installers",
    ".msi": "Installers",
    ".apk": "Installers",
    ".dmg": "Installers",
    ".deb": "Installers",
    ".rpm": "Installers",

    #Config / system
    ".ini": "Config",
    ".cfg": "Config",
    ".conf": "Config",
    ".env": "Config",
    ".log": "Logs",

    #Temporary / backups
    ".tmp": "Temp",
    ".bak": "Temp",
    ".old": "Temp",
}

def route_file(path: Path, conf: dict, category: str) -> Path | None:
    
    if not path.exists():
        logging.info(f"[SKIP] source is vanished: {path.name}")
        return None
    
    if not conf or "processed_path" not in conf:
        logging.error("[FAIL] Missing conf['processed_path']")
        return None

    dest_root = Path(conf["processed_path"])
    category_dir = dest_root / category
    dest_path = category_dir / path.name

    if dest_path.exists():
        i=1
        while True:
            candidate = category_dir / f"{path.stem}({i}){path.suffix}"
            if not candidate.exists():
                dest_path = candidate
                break
            i += 1
            
    if conf.get("dry_run", False):
            logging.info(f"DRY RUN: would ensure folder exists: {category_dir}")
            logging.info(f"DRY RUN: would move {path.name} -> {dest_path}")
            return dest_path
    
    try:
        category_dir.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError) as e:
        logging.error(f"Error occured when creating folder: {category} : {e}")
        return None
    
    
    try:
        path.replace(dest_path)
        logging.info(f"Moved {path.name} to {dest_path}")
        return dest_path
    except PermissionError:
        logging.error(f"Couldn't access {path.name}")
        return None
    except FileNotFoundError:
        logging.warning(f"The file isn't found: {path.name}")
        return None
    except OSError:
        logging.exception(f"[FAIL] OS error moving {path} -> {dest_path}")
        return None

    

def process_path(path: Path, eventType: str, dest: Path | None = None, conf=None) -> None:
    
    if eventType == "create":
        logging.info(f"Created file: {path.name}")
        category = EXTENSION_MAP.get(path.suffix.lower())
        if not category:
            category = "other"
            logging.warning(f"Unsupported extension: {path.suffix} routing to {category}. Consider adding to utils/processor.py/EXTENSION_MAP if needed ")
        route_file(path,conf,category)
        
    elif eventType == "modify":    
        logging.info(f"Modified file: {path.name}")
    elif eventType == "delete":
        logging.info(f"Deleted file: {path.name}")
    elif eventType == "move":
         logging.info(f"Moved/Renamed: {path.name} -> {dest.name if dest else ''}")

def process_folder_event(
    path: Path,
    event_type: str,
    dest: Path | None = None,
):
    if event_type == "create":
        logging.info(f"[FOLDER] Created: {path}")
    elif event_type == "move":
        logging.info(f"[FOLDER] Moved: {path} -> {dest}")
    elif event_type == "delete":
        logging.info(f"[FOLDER] Deleted: {path}")
    elif event_type == "modify":
        logging.info(f"[FOLDER] modified: {path}")

    