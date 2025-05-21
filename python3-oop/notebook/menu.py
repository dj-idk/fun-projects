import sys

from notebook import Notebook, Note


class Menu:
    """A simple menu system for managing notes"""

    def __init__(self):
        self.notebook = Notebook()
        self.choices = {
            "1": self.show_notes,
            "2": self.search_notes,
            "3": self.add_note,
            "4": self.modify_note,
            "5": self.quit,
        }

    def display_menu(self):
        print(
            """
Notebook Menu
              
1. Show all Notes
2. Search Notes
3. Add Note
4. Modify Note
5. Quit
"""
        )

    def run(self):
        """Display the menu and respond to user choices"""
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print(f"{choice} is not a valid choice. Please try again.")

    def show_notes(self, notes=None):
        if not notes:
            notes = self.notebook.notes
        for note in notes:
            print(f"{note.id}: {note.tags} \n{note.memo}")

    def search_notes(self):
        filter = input("Enter search term: ")
        notes = self.notebook.search(filter)
        self.show_notes(notes)

    def add_note(self):
        memo = input("Enter a memo: ")
        self.notebook.new_note(memo)
        print("Note added successfully.")

    def modify_note(self):
        id = int(input("Enter the note ID to modify: "))
        memo = input("Enter the new memo: ")
        tags = input("Enter the new tags (space-separated): ")
        if memo:
            self.notebook.modify_memo(id, memo)
        if tags:
            self.notebook.modify_tags(id, tags)

    def quit(self):
        """Exit the program"""
        print("Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    Menu().run()
