import sys
import datetime

from library import Library, Book, Member

members = [
    Member("John Smith", datetime.date(2020, 1, 15)),
    Member("Emma Johnson", datetime.date(2020, 3, 22)),
    Member("Michael Brown", datetime.date(2020, 5, 10)),
    Member("Sophia Williams", datetime.date(2020, 7, 5)),
    Member("Robert Davis", datetime.date(2020, 9, 18)),
]

books = [
    Book(
        "9780061120084",
        "To Kill a Mockingbird",
        "Harper Lee",
        datetime.date(1960, 7, 11),
    ),
    Book(
        "9780141439518",
        "Pride and Prejudice",
        "Jane Austen",
        datetime.date(1813, 1, 28),
    ),
    Book(
        "9780743273565",
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        datetime.date(1925, 4, 10),
    ),
    Book("9780451524935", "1984", "George Orwell", datetime.date(1949, 6, 8)),
    Book(
        "9780140283334",
        "The Catcher in the Rye",
        "J.D. Salinger",
        datetime.date(1951, 7, 16),
    ),
    Book(
        "9780316769174",
        "The Lord of the Rings",
        "J.R.R. Tolkien",
        datetime.date(1954, 7, 29),
    ),
    Book("9780062315007", "The Alchem0t", "Paulo Coelho", datetime.date(1988, 1, 1)),
    Book(
        "9780307474278",
        "The Kite Runner",
        "Khaled Hosseini",
        datetime.date(2003, 5, 29),
    ),
    Book(
        "9780143105428",
        "The Picture of Dorian Gray",
        "Oscar Wilde",
        datetime.date(1890, 7, 1),
    ),
    Book(
        "9780679783268",
        "Crime and Punishment",
        "Fyodor Dostoevsky",
        datetime.date(1866, 1, 1),
    ),
]


class LibraryManagementSystem:
    """A menu system for managing a library"""

    def __init__(self):
        self.library = Library()
        self.choices = {"1": self.member_menu, "2": self.book_menu, "3": self.quit}
        self.library.books.extend(books)
        self.library.members.extend(members)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")

    def display_menu(self):
        print(
            """
Library Management System

1. Manage library members
2. Manage library books
3. Quit
"""
        )

    def member_menu(self):
        menu = self.MemberMenu(self.library)
        menu.run()

    def book_menu(self):
        menu = self.BookMenu(self.library)
        menu.run()

    def quit(self):
        print("Goodbye!")
        sys.exit(0)

    class BookMenu:
        """A menu for managing library Books"""

        def __init__(self, library):
            self.library = library
            self.choices = {
                "0": self.show_books,
                "1": self.add_book,
                "2": self.edit_book,
                "3": self.remove_book,
                "4": self.search_books,
                "5": self.find_book_by_isbn,
                "6": self.lend_book,
                "7": self.receive_book,
                "8": self.back,
            }

        def run(self):
            while True:
                self.display_menu()
                choice = input("Enter your choice: ")
                action = self.choices.get(choice)
                if action:
                    action()
                    if choice == "8":
                        break
                else:
                    print("Invalid choice. Please try again.")

        def display_menu(self):
            """Display the menu for managing library books"""
            print(
                """
Book Menu

0. Show all books
1. Add a new book
2. Edit book details
3. Remove a book
4. Search for books by title, author, or publication date
5. Find book by ISBN
6. Lend a book
7. Receive a borrowed book
8. Back to main menu

"""
            )

        def show_books(self):
            """Display all books in the library"""
            self.library.display_books()

        def add_book(self):
            """Add a new book"""
            isbn = input("Enter the ISBN of the book: ")
            title = input("Enter the title of the book: ")
            author = input("Enter the author of the book: ")
            try:
                publication_date = input("Enter the publication date (YYYY-MM-DD): ")
                date_obj = datetime.datetime.strptime(
                    publication_date, "%Y-%m-%d"
                ).date()
                book = Book(isbn, title, author, date_obj)
                self.library.add_book(book)
                print("Book added successfully.")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        def edit_book(self):
            """Edit book details"""
            isbn = input("Enter the ISBN of the book to edit: ")
            title = input("Enter the new title of the book: ")
            author = input("Enter the new author of the book: ")
            try:
                publication_date = input(
                    "Enter the new publication date (YYYY-MM-DD): "
                )
                date_obj = datetime.datetime.strptime(
                    publication_date, "%Y-%m-%d"
                ).date()
                self.library.edit_book(isbn, title, author, date_obj)
                print("Book details edited successfully.")
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

        def remove_book(self):
            """Remove a book"""
            isbn = input("Enter the ISBN of the book to remove: ")
            self.library.remove_book(isbn)
            print("Book removed successfully.")

        def search_books(self):
            """Search for books by title, author, or publication date"""
            query = input("Enter the search query: ")
            results = self.library.search_books(query)
            if results:
                for book in results:
                    print(book)
            else:
                print("No books found.")

        def find_book_by_isbn(self):
            """Find a book by ISBN"""
            isbn = input("Enter the ISBN of the book: ")
            book = self.library.find_book_by_isbn(isbn)
            if book:
                print(book)
            else:
                print("Book not found.")

        def lend_book(self):
            """Lend a book"""
            isbn = input("Enter the ISBN of the book to lend: ")
            try:
                member_id = int(input("Enter the member ID: "))
                self.library.lend_book(isbn, member_id)
                print("Book lent successfully.")
            except ValueError:
                print("Invalid member ID. Please enter a number.")

        def receive_book(self):
            """Receive a borrowed book"""
            isbn = input("Enter the ISBN of the book to receive: ")
            try:
                member_id = int(input("Enter the member ID: "))
                self.library.receive_book(isbn, member_id)
                print("Book received successfully.")
            except ValueError:
                print("Invalid member ID. Please enter a number.")

        def back(self):
            """Return to main menu"""
            pass

    class MemberMenu:
        """A menu for managing library members"""

        def __init__(self, library):
            self.library = library
            self.choices = {
                "0": self.show_members,
                "1": self.add_member,
                "2": self.edit_member,
                "3": self.remove_member,
                "4": self.search_members,
                "5": self.find_member_by_id,
                "6": self.back,
            }

        def run(self):
            while True:
                self.display_menu()
                choice = input("Enter your choice: ")
                action = self.choices.get(choice)
                if action:
                    action()
                    if choice == "6":  # Back to main menu
                        break
                else:
                    print("Invalid choice. Please try again.")

        def display_menu(self):
            """Display the menu for managing library members"""
            print(
                """
Member Menu

0. Show all members
1. Add a new member
2. Edit member details
3. Remove a member
4. Search for members by name or registration date
5. Find member by ID
6. Back to main menu

"""
            )

        def show_members(self):
            """Display all members in the library"""
            self.library.display_members()

        def add_member(self):
            """Add a new member"""
            name = input("Enter the name of the member: ")
            member = Member(name, datetime.datetime.now().date())
            self.library.add_member(member)
            print("Member added successfully.")

        def edit_member(self):
            """Edit member details"""
            try:
                member_id = int(input("Enter the member ID to edit: "))
                name = input("Enter the new name of the member: ")
                self.library.edit_member(member_id, name)
                print("Member details edited successfully.")
            except ValueError:
                print("Invalid member ID. Please enter a number.")

        def remove_member(self):
            """Remove a member"""
            try:
                member_id = int(input("Enter the member ID to remove: "))
                self.library.remove_member(member_id)
                print("Member removed successfully.")
            except ValueError:
                print("Invalid member ID. Please enter a number.")

        def search_members(self):
            """Search for members by name or registration date"""
            query = input("Enter the search query: ")
            results = self.library.search_members(query)
            if results:
                for member in results:
                    print(member)
            else:
                print("No members found.")

        def find_member_by_id(self):
            """Find a member by ID"""
            try:
                member_id = int(input("Enter the member ID: "))
                member = self.library.find_member_by_id(member_id)
                if member:
                    print(member)
                else:
                    print("Member not found.")
            except ValueError:
                print("Invalid member ID. Please enter a number.")

        def back(self):
            """Return to main menu"""
            pass


if __name__ == "__main__":
    LibraryManagementSystem().run()
1
