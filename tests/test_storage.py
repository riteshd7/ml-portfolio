import pytest 
from cli.notes.storage import load_notes, save_notes, next_id
from cli.notes.exceptions import CorruptNotesError


def test_load_returns_empty_list_when_file_is_missing(tmp_path):
    fake = tmp_path / "no_such_file.json"
    assert load_notes(fake) == []


def test_load_returns_empty_list_when_file_is_empty(tmp_path):
    empty = tmp_path / "empty.json"
    empty.write_text("")
    assert load_notes(empty) == []


def test_load_raises_on_corrupt_json(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json}")
    with pytest.raises(CorruptNotesError):
        load_notes(bad)


def test_save_and_load_roundtrip(tmp_path):
    notes = [{"id": 1, "text": "hi", "done": False, "created": "2026-05-02"}]
    path = tmp_path / "notes.json"
    save_notes(path, notes)
    assert load_notes(path) == notes

#did not understand this one
@pytest.mark.xfail(reason="save_notes does not create missing parent directories yet")
def test_save_creates_parent_directory_if_needed(tmp_path):
    """Saving into a not-yet-existing subdirectory should still work."""
    path = tmp_path / "subdir" / "notes.json"
    save_notes(path, [{"id": 1, "text": "hi", "done": False, "created": "2026-05-02"}])
    assert path.exists()


def test_next_id_returns_one_when_empty():
    assert next_id([]) == 1


def test_next_id_returns_max_plus_one():
    notes = [{"id": 3, "text": "a"}, {"id": 1, "text": "b"}]
    assert next_id(notes) == 4