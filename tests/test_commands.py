import pytest
from cli.notes.commands import cmd_add, cmd_list, cmd_done, cmd_rm
from cli.notes.exceptions import EmptyTextError, NoteNotFoundError
from cli.notes.storage import load_notes


def test_cmd_add_creates_note_and_prints_confirmation(tmp_path, capsys):
    path = tmp_path / "notes.json"
    cmd_add(path, "buy milk")
    notes = load_notes(path)
    assert len(notes) == 1
    assert notes[0]["text"] == "buy milk"
    assert notes[0]["done"] is False
    out = capsys.readouterr().out
    assert "Added note 1" in out


def test_cmd_add_raises_on_empty_text(tmp_path):
    path = tmp_path / "notes.json"
    with pytest.raises(EmptyTextError):
        cmd_add(path, "")


def test_cmd_list_prints_no_notes_message_when_empty(tmp_path, capsys):
    path = tmp_path / "notes.json"
    cmd_list(path)
    out = capsys.readouterr().out
    assert "No notes yet." in out


def test_cmd_list_prints_each_note(tmp_path, capsys):
    path = tmp_path / "notes.json"
    cmd_add(path, "first")
    cmd_add(path, "second")
    capsys.readouterr()  # discard the "Added note" output from setup above
    cmd_list(path)
    out = capsys.readouterr().out
    assert "first" in out
    assert "second" in out


def test_cmd_done_marks_note_done(tmp_path):
    path = tmp_path / "notes.json"
    cmd_add(path, "buy milk")
    cmd_done(path, 1)
    notes = load_notes(path)
    assert notes[0]["done"] is True


def test_cmd_done_raises_when_note_missing(tmp_path):
    path = tmp_path / "notes.json"
    with pytest.raises(NoteNotFoundError):
        cmd_done(path, 999)


def test_cmd_rm_removes_note(tmp_path):
    path = tmp_path / "notes.json"
    cmd_add(path, "buy milk")
    cmd_rm(path, 1)
    assert load_notes(path) == []


def test_cmd_rm_raises_when_note_missing(tmp_path):
    path = tmp_path / "notes.json"
    with pytest.raises(NoteNotFoundError):
        cmd_rm(path, 999)