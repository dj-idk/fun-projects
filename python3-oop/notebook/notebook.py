import datetime

last_id = 0


class Note:
    """Represents a note in a notebook.
    Match against a string in searches and store tags for each notes."""

    def __init__(self, memo, tags=""):
        """intitlaize a new note with memo and optional space-separated tags.
        Automatically set note's creattion date and unique id."""
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.date.today()
        global last_id
        last_id += 1
        self.id = last_id

    def match(self, filter):
        """Determine if this note matches the given filter string.
        Return True if it matches, False otherwise.

        Search is case sensitive and matches both text and tags.
        """
        return filter in self.memo or filter in self.tags


class Notebook:
    """Represents collection of notes that can be tagged,
    modified, and searched."""

    def __init__(self):
        self.notes = []

    def new_note(self, memo, tags=""):
        """Create a new note and add it to the list."""
        self.notes.append(Note(memo, tags))

    def _find_note(self, note_id):
        """Find a note by its id."""
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    def modify_memo(self, note_id, memo):
        """Modify the memo of a note by its id."""
        note = self._find_note(note_id)
        if note:
            note.memo = memo
            return True
        return False

    def modify_tags(self, note_id, tags):
        """Modify the tags of a note by its id."""
        note = self._find_note(note_id)
        if note:
            note.tags = tags
            return True
        return False

    def search(self, filter):
        """Search for notes that match the given filter string.
        Return a list of matching notes."""
        return [note for note in self.notes if note.match(filter)]
