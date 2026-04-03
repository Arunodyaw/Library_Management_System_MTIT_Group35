# book-service/data_service.py
from models import Book, BookCreate, BookUpdate

class BookMockDataService:
    def __init__(self):
        self.books = [
            Book(id=1, book_title="The Alchemist", book_type="Fiction", author="Paulo Coelho", isbn="9780061122415", publisher="HarperOne", book_price=15.99),
            Book(id=2, book_title="Clean Code", book_type="Programming", author="Robert C. Martin", isbn="9780132350884", publisher="Prentice Hall", book_price=32.50),
            Book(id=3, book_title="1984", book_type="Dystopian", author="George Orwell", isbn="9780451524935", publisher="Signet Classics", book_price=12.99),
        ]
        self.next_id = 4

    # Get all books
    def get_all_books(self):
        return self.books

    # Get book by ID
    def get_book_by_id(self, book_id: int):
        return next((b for b in self.books if b.id == book_id), None)

    # Add a new book
    def add_book(self, book_data: BookCreate):
        new_book = Book(id=self.next_id, **book_data.dict())
        self.books.append(new_book)
        self.next_id += 1
        return new_book

    # Update existing book
    def update_book(self, book_id: int, book_data: BookUpdate):
        book = self.get_book_by_id(book_id)
        if book:
            update_data = book_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(book, key, value)
            return book
        return None

    # Delete a book
    def delete_book(self, book_id: int):
        book = self.get_book_by_id(book_id)
        if book:
            self.books.remove(book)
            return True
        return False