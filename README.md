# Watchdog File Processor

This project is a Python based folder‑watching automation tool that monitors a target directory and automatically organizes new files into a structured output location.

---

## How It Works

- Watches a directory for file creation, modification, movement, and deletion events
- Waits until files are stable before processing them
- Moves files into a processed directory -> categorized by extension
- Logs all actions and errors
- Can run in dry-run mode to preview behavior without modifying the filesystem

The folders named `Incoming` and `processed` are only examples. Any paths can be used.

---

## Configuration

All behavior is controlled through `config.json`.
Example configuration:

```json
{
  "watch_path": "Incoming",
  "processed_path": "processed",

  "dry_run": false,
  "recursive": false,

  "log_file": "watch_folder.log",
  "log_level": "INFO"
}
```
## Configuration Parameters

* watch_path -> Path to the folder that will be monitored for incoming files. Can be an absolute path or a path relative to the project root.
* processed_path -> Destination folder where processed files will be moved. If the path is relative, it will be resolved relative to the project root.
* dry_run -> When set to true, no files or folders are created or moved. All actions are logged as "would do" operations.
* recursive -> When true, subfolders inside the watched directory are also monitored. When false, only the top-level folder is watched.
* log_file -> Path to the log file where all activity is recorded.
* log_level -> Logging verbosity level. Common values are: INFO, WARNING, ERROR, DEBUG

## How to Run
- Create and activate a virtual environment (recommended)
- Install dependency: `pip install watchdog`
- Adjust config.json as needed
- Run the program: `python main.py`

The program will keep running and monitoring the folder until manually stopped (use q or CTRL + C)


