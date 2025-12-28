from __future__ import annotations
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from utils.processor import process_path
from utils.processor import process_folder_event
from threading import Timer, Lock
from utils.stability import wait_until_stable
import logging

class DebouncedHandler(FileSystemEventHandler):
    def __init__(self,conf, debounce_seconds: float = 0.8):
        self.conf = conf
        self.debounce_seconds = debounce_seconds
        self._lock = Lock()

        # key: path (string), value: Timer
        self._timers: dict[str, Timer] = {}

        # store the latest event info per path
        self._latest: dict[str, dict] = {}

    def _schedule_file(self, src: Path, event_type: str, dest: Path | None = None):
        key_path = dest if (event_type == "move" and dest is not None) else src
        key = str(key_path)
        #key = str(src)

        def fire():
            # take the latest snapshot atomically
            with self._lock:
                data = self._latest.pop(key, None)
                self._timers.pop(key, None)

            if not data:
                return

            src_ = data["src"]
            event_type_ = data["event_type"]
            dest_ = data.get("dest")

            effective_path = dest_ if (event_type_ == "move" and dest_ is not None) else src_   

            if event_type in {"create", "modify", "move"}:
                logging.info(f"[WAIT] Checking stability: {effective_path.name}")
                if not wait_until_stable(effective_path,conf=self.conf):
                    logging.warning(f"[Skip] File not stable or vanished: {effective_path.name}")
                    return

            process_path(src,event_type,dest=dest, conf=self.conf)

        with self._lock:
            # update latest event info
            self._latest[key] = {"src": src, "event_type": event_type, "dest": dest}

            # reset timer
            old = self._timers.get(key)
            if old:
                old.cancel()

            t = Timer(self.debounce_seconds, fire)
            t.daemon = True
            self._timers[key] = t
            t.start()
        
    def on_created(self, event):
        p = Path(event.src_path)
        if event.is_directory:
            process_folder_event(p, "create")
            return
        self._schedule_file(p, "create")

    def on_moved(self, event):
        p = Path(event.src_path)
        dest = Path(event.dest_path)
        if event.is_directory:
            process_folder_event(p, "move", dest)
            return
        self._schedule_file(p, "move", dest)

    def on_modified(self, event):
        p = Path(event.src_path)
        if event.is_directory:
            process_folder_event(p, "modify",)
            return
        self._schedule_file(p,"modify")

    def on_deleted(self, event):
        p = Path(event.src_path)
        if event.is_directory:
            process_folder_event(p, "delete",)
            return
        self._schedule_file(p, "delete")

def watch(path: Path, conf, recursive: bool = True):
    observer = Observer()
    handler = DebouncedHandler(conf,debounce_seconds=0.8)
    observer.schedule(handler, str(path), recursive=recursive)
    observer.start()

    try:
        while True:
            cmd = input("Type 'q' to quit: ").strip().lower()
            if cmd == "q":
                break
    finally:
        observer.stop()
        observer.join()
    