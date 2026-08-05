import argparse
import sys 

from .commands import cmd_add, cmd_done, cmd_list, cmd_rm
from .exceptions import NoteNotFoundError, EmptyTextError
from .storage import NOTES_FILE

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
            cmd_add(NOTES_FILE, args.text)
        elif args.command == "list":
            cmd_list(NOTES_FILE)
        elif args.command == "done":
            cmd_done(NOTES_FILE, args.note_id)
        elif args.command == "rm":
            cmd_rm(NOTES_FILE, args.note_id)
    except NoteNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except EmptyTextError as e:
        # Catches empty text and prints a clean error
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


