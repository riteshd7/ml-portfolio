"NOTES CLI"

import json 
from pathlib import Path
from datetime import date
import sys
import argparse


NOTES_FILE = Path.home() / ".notes.json"     

class NoteNotFoundError(Exception):
    pass

def load_notes():
    
    if not NOTES_FILE.exists():
        return []
    
    with open(NOTES_FILE , "r" , encoding = "utf-8") as f:
        return json.load(f)

def save_notes(notes):

    with open(NOTES_FILE , "w" , encoding = "utf-8") as f:
        json.dump(notes , f)
    
    
def next_id(notes):
    
    if not notes:
        return 1 
    
    return max(note["id"] for note in notes) + 1 

def cmd_add(text):

    notes = load_notes()
    new_id  = next_id(notes)    

    new_note = {
        "id": new_id,
        "text": text,
        "done": False,
        "created": date.today().isoformat()
    }

    notes.append(new_note)  
    save_notes(notes)

    print(f"Added note {new_id} : {text}")


def cmd_list():
    notes = load_notes()
    if not notes:
        print("No notes yet")
        return 
    
    for note in notes:
        status_char = "x" if note["done"] else ""
        print((f"{note['id']}. [{status_char}] {note['text']} (added {note['created']})"))


def cmd_done(note_id):
    notes = load_notes()
    for note in notes:
        if note["id"] == note_id:
            note["done"] = True
            save_notes(notes)
            print(f"Marked note {note_id} as done")
            return 
    
    raise NoteNotFoundError(f"No note found with id {note_id} (run 'notes list' to see ids)")       


def cmd_rm(note_id):
    
    notes = load_notes()
    for i, note in enumerate(notes):
        if note["id"] == note_id:
            notes.pop(i)
            save_notes(notes)
            print(f"Removed note{note_id}")
            return
    
    raise NoteNotFoundError(f"No such note found with id{note_id}")

def build_parser():
    
    parser = argparse.ArgumentParser(prog ="notes")
    sub = parser.add_subparsers(dest = "command")

    p_add = sub.add_parser("add")
    p_add.add_argument("text")

    if not args.text.strip():
        parser.error("note text cannot be empty")    # argparse exits with proper error

    p_list = sub.add_parser("list") 

    p_done = sub.add_parser("done")
    p_done.add_argument("note_id", type = int)  

    p_rm = sub.add_parser("rm", help="remove a note")
    p_rm.add_argument("note_id", type = int)

    return parser           

def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add" and not args.text.strip():
        parser.error("note text cannot be empty")   
    
    try:
        if args.command =="add":
            cmd_add(args.text)  
        elif args.command == "list":
            cmd_list()
        elif args.command == "done":
            cmd_done(args.note_id)
        elif args.command == "rm":
            cmd_rm(args.note_id)    
    except NoteNotFoundError as e:

        print(f"Error: {e}, file = sys.stderr")
        sys.exit(1)

if __name__ == "__main__":
    main()  



