class NoteNotFoundError(Exception):
    """Raised when a referenced note id doesn't exist."""
class EmptyTextError(Exception):
    """Raised when a text is empty.""" 
class CorruptNotesError(Exception):
    """Raised when the notes file exists but contains invalid JSON."""

