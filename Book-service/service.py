# book-service/service.py
from data_service import BookMockDataService
from models import BookCreate, BookUpdate

class BookService:
    def __init__(self):
        self.data_service = BookMockDataService()

    # Get all books
    def get_all(self):
        return self.data_service.get_all_books()

    # Get book by ID
    def get_by_id(self, book_id: int):
        return self.data_service.get_book_by_id(book_id)

    # Create a new book
    def create(self, book_data: BookCreate):
        return self.data_service.add_book(book_data)

    # Update an existing book
    def update(self, book_id: int, book_data: BookUpdate):
        return self.data_service.update_book(book_id, book_data)

    # Delete a book
    def delete(self, book_id: int):
        return self.data_service.delete_book(book_id)