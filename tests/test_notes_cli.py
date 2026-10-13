import pytest
from cli.notes.cli import build_parser, main


def test_build_parser_parses_add_command():
    parser = build_parser()
    args = parser.parse_args(["add", "buy milk"])
    assert args.command == "add"
    assert args.text == "buy milk"


def test_build_parser_requires_a_command():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_main_add_writes_a_note(tmp_path, monkeypatch, capsys):
    notes_file = tmp_path / "notes.json"
    monkeypatch.setattr(
        "sys.argv", ["notes", "--file", str(notes_file), "add", "buy milk"]
    )
    main()
    out = capsys.readouterr().out
    assert "Added note 1" in out
    assert notes_file.exists()


def test_main_rejects_whitespace_only_text(tmp_path, monkeypatch):
    notes_file = tmp_path / "notes.json"
    monkeypatch.setattr(
        "sys.argv", ["notes", "--file", str(notes_file), "add", "   "]
    )
    with pytest.raises(SystemExit):
        main()


def test_main_done_on_missing_note_exits_with_error(tmp_path, monkeypatch, capsys):
    notes_file = tmp_path / "notes.json"
    monkeypatch.setattr(
        "sys.argv", ["notes", "--file", str(notes_file), "done", "5"]
    )
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
    err = capsys.readouterr().err
    assert "no note with id 5" in err


def test_main_list_prints_added_note(tmp_path, monkeypatch, capsys):
    notes_file = tmp_path / "notes.json"
    monkeypatch.setattr(
        "sys.argv", ["notes", "--file", str(notes_file), "add", "buy milk"]
    )
    main()
    capsys.readouterr()  # discard the "Added note" output from setup above

    monkeypatch.setattr("sys.argv", ["notes", "--file", str(notes_file), "list"])
    main()
    out = capsys.readouterr().out
    assert "buy milk" in out