last_id = 0


class Member:
    """Represents a member of a library."""

    def __init__(self, full_name, date_joined):
        global last_id
        last_id += 1
        self.id = last_id
        self.full_name = full_name
        self.date_joined = date_joined
        self.borrowed_books = []

    def __str__(self):
        """Returns a string representation of the member."""
        return f"Member ID: {self.id}, Name: {self.full_name}, Date Joined: {self.date_joined.strftime('%B %d, %Y, %H:%M:%S')}"

    def borrow_book(self, book):
        """Borrow a book from the library."""
        if not book.borrowed:
            self.borrowed_books.append(book)
            book.borrow()
            print(f"{self.full_name} has borrowed {book.title}")

    def return_book(self, book):
        """Return a borrowed book to the library."""
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)
            book.return_book()
            print(f"{self.full_name} has returned {book.title}")
        else:
            print(f"{self.full_name} has not borrowed {book.title}")

    def match(self, query):
        """Matches the member's name with the query string."""
        if query.lower() in self.full_name.lower():
            return True
        return False
