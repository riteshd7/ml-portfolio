import argparse
import sys 

from .commands import cmd_add, cmd_done, cmd_list, cmd_rm
from .exceptions import NoteNotFoundError, EmptyTextError
from .storage import NOTES_FILE
from pathlib import Path

def build_parser():
    parser = argparse.ArgumentParser(prog="notes", description="A tiny note manager")
    parser.add_argument("--file" , type = Path, default= None, help = "path to notes file (default: ~/.notes.json)")
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
    notes_file = args.file or NOTES_FILE

    if args.command == "add" and not args.text.strip():
        parser.error("note text cannot be empty")

    try:
        if args.command == "add":
            cmd_add(notes_file, args.text)
        elif args.command == "list":
            cmd_list(notes_file)
        elif args.command == "done":
            cmd_done(notes_file, args.note_id)
        elif args.command == "rm":
            cmd_rm(notes_file, args.note_id)
    except NoteNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except EmptyTextError as e:
        # Catches empty text and prints a clean error
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


