"""Notes CLI - a tiny command-line note manager."""


import argparse
import json 
import sys
from datetime import date
from pathlib import Path
#relative import of exception       
from .exceptions import NoteNotFoundError
#relative imports of storage 
from .storage import load_notes, save_notes, next_id, NOTES_FILE


class EmptyTextError(Exception):
    """Raised when a text is empty."""  

def cmd_add(text):
    notes = load_notes(NOTES_FILE)
    if not text:
            raise EmptyTextError(f"text is empty)")
    note = {
        "id": next_id(notes),
        "text": text,
        "done": False,
        "created": str(date.today())
    }
    notes.append(note)
    save_notes(NOTES_FILE, notes)
    print(f"Added note {note['id']}: {note['text']}")


def cmd_list():
    notes = load_notes(NOTES_FILE)
    if not notes:
        print("No notes yet.")
        return
    for note in notes:
        status_char = "x" if note["done"] else " "
        print(f"{note['id']}. [{status_char}] {note['text']}  (added {note['created']})")


def cmd_done(note_id):
    notes = load_notes(NOTES_FILE)
    for note in notes:
        if note["id"] == note_id:
            note["done"] = True
            save_notes(NOTES_FILE, notes)
            print(f"Marked note {note_id} as done.")
            return
    raise NoteNotFoundError(f"no note with id {note_id} (run `notes list` to see ids)")


def cmd_rm(note_id):
    notes = load_notes(NOTES_FILE)
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

    if args.command == "add" and not args.text.strip():
        parser.error("note text cannot be empty")

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



