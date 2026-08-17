import json
from pathlib import Path
import sys

NOTES_FILE = Path.home() / ".notes.json"

def load_notes(path):
    """Read notes from disk. Return [] if file doesn't exist."""
    if not path.exists():
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {path} contains corrupt JSON. Fix or remove it and try again.",
              file=sys.stderr)
        sys.exit(1)

def save_notes(path, notes):
    """Write notes to disk."""
    with open(path, "w") as f:
        json.dump(notes, f, indent=2)

def next_id(notes):
    """Return max existing id + 1, or 1 if empty."""
    if not notes:
        return 1
    return max(note["id"] for note in notes) + 1