import datetime

from member import Member


class Book:
    """A book in the library."""

    def __init__(
        self, isbn: str, title: str, author: str, publication_date: datetime.date
    ):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.borrowed = False

    def __str__(self):
        return f"<{self.title} by {self.author}, published at: {self.publication_date}, ISBN: {self.isbn}>, borrowed: {self.borrowed}>"

    def match(self, query: str) -> bool:
        return query.lower() in str(str(self)).lower()

    def borrow(self):
        if not self.borrowed:
            self.borrowed = True
            return True
        else:
            return False

    def return_book(self):
        if self.borrowed:
            self.borrowed = False
            return True
        else:
            return False


class Library:
    """A library with books and members."""

    def __init__(self):
        self.books = []
        self.borrowed_books = []
        self.members = []

    # ---------- Book management ----------

    def _find_book_by_isbn(self, isbn: str) -> Book:
        """Find a book by its ISBN."""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def add_book(self, book: Book):
        """Add a book to the library."""
        self.books.append(book)
        print(f"Book '{book.title}' added to the library.")

    def edit_book(
        self, isbn: str, title: str, author: str, publication_date: datetime.date
    ):
        """Edit a book's details by its ISBN."""
        book = self._find_book_by_isbn(isbn)
        if book:
            book.title = title
            book.author = author
            book.publication_date = publication_date
            print(f"Book '{book.title}' edited.")
        print("Book not found.")

    def search_books(self, query: str) -> list:
        """Search for books by a query."""
        return [book for book in self.books if book.match(query)]

    def lend_book(self, isbn: str, member_id: int):
        """Lend a book to a member by its ISBN and member ID."""
        book = self._find_book_by_isbn(isbn)
        member = self._find_member_by_id(member_id)
        if book and not book.borrowed and member:
            book.borrow()
            self.borrowed_books.append(book)
            member.borrow_book(book)
            print(f"Book '{book.title}' borrowed by {member.full_name}.")
        print("Book not found or already borrowed.")

    def recieve_book(self, isbn: str, member_id: int):
        """Receive a book from a member by its ISBN and member ID."""
        book = self._find_book_by_isbn(isbn)
        member = self._find_member_by_id(member_id)
        if book and book.borrowed and member:
            book.return_book()
            self.borrowed_books.remove(book)
            member.return_book(book)
            print(f"Book '{book.title}' returned by {member.full_name}.")
        print("Book not found or not borrowed.")

    def display_books(self):
        """Display all books in the library."""
        print("Books in the library:")
        for book in self.books:
            print(f"- {str(book)}")

    # ---------- Member management ----------

    def _find_member_by_id(self, member_id: int) -> Member:
        """Find a member by their ID."""
        for member in self.members:
            if member.id == member_id:
                return member
        return None

    def add_member(self, member: Member):
        """Add a member to the library."""
        self.members.append(member)
        print(f"Member '{member.full_name}' added to the library.")

    def edit_member(self, member_id: int, full_name: str):
        """Edit a member's details by their ID."""
        member = self._find_member_by_id(member_id)
        if member:
            member.full_name = full_name
            print(f"Member '{member.full_name}' edited.")
        print("Member not found.")

    def search_members(self, query: str) -> list:
        """Search for members by a query."""
        return [member for member in self.members if member.match(query)]

    def remove_member(self, member_id: int):
        """Remove a member from the library by their ID."""
        member = self._find_member_by_id(member_id)
        if member:
            self.members.remove(member)
            print(f"Member '{member.full_name}' removed from the library.")
        print("Member not found.")

    def display_members(self):
        """Display all members in the library."""
        print("Members in the library:")
        for member in self.members:
            print(f"- {str(member)}")
