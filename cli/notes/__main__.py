"""Notes CLI - a tiny command-line note manager."""

import argparse
import json
import sys
from datetime import date
from pathlib import Path

NOTES_FILE = Path.home() / ".notes.json"


class NoteNotFoundError(Exception):
    """Raised when a referenced note id doesn't exist."""
class EmptyTextError(Exception):
    """Raised when a text is empty."""  


def load_notes():
    """Read notes from disk. Return [] if file doesn't exist."""
    if not NOTES_FILE.exists():
        return []
    try:
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {NOTES_FILE} contains corrupt JSON. Fix or remove it and try again.",
              file=sys.stderr)
        sys.exit(1)


def save_notes(notes):
    """Write notes to disk."""
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)


def next_id(notes):
    """Return max existing id + 1, or 1 if empty."""
    if not notes:
        return 1
    return max(note["id"] for note in notes) + 1


def cmd_add(text):
    notes = load_notes()
    if not text:
            raise EmptyTextError(f"text is empty)")
    note = {
        "id": next_id(notes),
        "text": text,
        "done": False,
        "created": str(date.today()),
    }
    notes.append(note)
    save_notes(notes)
    print(f"Added note {note['id']}: {note['text']}")


def cmd_list():
    notes = load_notes()
    if not notes:
        print("No notes yet.")
        return
    for note in notes:
        status_char = "x" if note["done"] else " "
        print(f"{note['id']}. [{status_char}] {note['text']}  (added {note['created']})")


def cmd_done(note_id):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            note["done"] = True
            save_notes(notes)
            print(f"Marked note {note_id} as done.")
            return
    raise NoteNotFoundError(f"no note with id {note_id} (run `notes list` to see ids)")


def cmd_rm(note_id):
    notes = load_notes()
    filtered = [note for note in notes if note["id"] != note_id]
    if len(filtered) == len(notes):
        raise NoteNotFoundError(f"no note with id {note_id} (run `notes list` to see ids)")
    save_notes(filtered)
    print(f"Removed note {note_id}.")


def build_parser():
    parser = argparse.ArgumentParser(prog="notes", description="A tiny note manager")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a note")
    p_add.add_argument("text", help="the note text")

    sub.add_parser("list", help="list all notes")

    p_done = sub.add_parser("done", help="mark a note done")
    p_done.add_argument("note_id", type=int)

    p_rm = sub.add_parser("rm", help="remove a note")
    p_rm.add_argument("note_id", type=int)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    #if args.command == "add" and not args.text.strip():
    #    parser.error("note text cannot be empty")

    try:
        if args.command == "add":
            cmd_add(args.text)
        elif args.command == "list":
            cmd_list()
        elif args.command == "done":
            cmd_done(args.note_id)
        elif args.command == "rm":
            cmd_rm(args.note_id)
    except NoteNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


