import datetime

from member import Member


class Book:
    def __init__(
        self, isbn: str, title: str, author: str, publication_date: datetime.date
    ):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.borrowed = False

    def __str__(self):
        return f"<{self.title} by {self.author}, published at: {self.publication_date}, ISBN: {self.isbn}>"

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
    def __init__(self):
        self.books = []
        self.borrowed_books = []
        self.memebers = []

    def _find_book_by_isbn(self, isbn: str) -> Book:
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def _find_member_by_id(self, member_id: int) -> Member:
        for member in self.members:
            if member.id == member_id:
                return member
        return None

    def add_book(self, book: Book):
        self.books.append(book)
        print(f"Book '{book.title}' added to the library.")

    def edit_book(
        self, isbn: str, title: str, author: str, publication_date: datetime.date
    ):
        book = self._find_book_by_isbn(isbn)
        if book:
            book.title = title
            book.author = author
            book.publication_date = publication_date
            print(f"Book '{book.title}' edited.")
        print("Book not found.")

    def search_books(self, query: str) -> list:
        return [book for book in self.books if book.match(query)]

    def lend_book(self, isbn: str, member_id: int):
        book = self._find_book_by_isbn(isbn)
        member = self._find_member_by_id(member_id)
        if book and not book.borrowed and member:
            book.borrow()
            self.borrowed_books.append(book)
            member.borrow_book(book)
            print(f"Book '{book.title}' borrowed by {member.full_name}.")
        print("Book not found or already borrowed.")

    def recieve_book(self, isbn: str, member_id: int):
        book = self._find_book_by_isbn(isbn)
        member = self._find_member_by_id(member_id)
        if book and book.borrowed and member:
            book.return_book()
            self.borrowed_books.remove(book)
            member.return_book(book)
            print(f"Book '{book.title}' returned by {member.full_name}.")
        print("Book not found or not borrowed.")
