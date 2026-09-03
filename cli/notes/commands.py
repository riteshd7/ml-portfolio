from datetime import date
from .exceptions import NoteNotFoundError,EmptyTextError
from .storage import load_notes, save_notes, next_id
#from pathlib import Path  

#NOTES_FILE = Path.home() / ".notes.json"

def cmd_add(notes_file, text):
    notes = load_notes(notes_file)
    if not text:
            raise EmptyTextError(f"text is empty")
    note = {
        "id": next_id(notes),
        "text": text,
        "done": False,
        "created": str(date.today())
    }
    notes.append(note)
    save_notes(notes_file, notes)
    print(f"Added note {note['id']}: {note['text']}")


def cmd_list(notes_file):
    notes = load_notes(notes_file)
    if not notes:
        print("No notes yet.")
        return
    for note in notes:
        status_char = "x" if note["done"] else " "
        print(f"{note['id']}. [{status_char}] {note['text']}  (added {note['created']})")


def cmd_done(notes_file, note_id):
    notes = load_notes(notes_file)
    for note in notes:
        if note["id"] == note_id:
            note["done"] = True
            save_notes(notes_file, notes)
            print(f"Marked note {note_id} as done.")
            return
    raise NoteNotFoundError(f"no note with id {note_id} (run `notes list` to see ids)")


def cmd_rm(notes_file, note_id):
    notes = load_notes(notes_file)
    filtered = [note for note in notes if note["id"] != note_id]
    if len(filtered) == len(notes):
        raise NoteNotFoundError(f"no note with id {note_id} (run `notes list` to see ids)")
    save_notes(notes_file,filtered)
    print(f"Removed note {note_id}.")