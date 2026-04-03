# book-service/models.py
from pydantic import BaseModel
from typing import Optional

# Main Book model
class Book(BaseModel):
    id: int
    book_title: str
    book_type: str
    author: str
    isbn: str
    publisher: str
    book_price: float

# Model for creating a new book
class BookCreate(BaseModel):
    book_title: str
    book_type: str
    author: str
    isbn: str
    publisher: str
    book_price: float

# Model for updating an existing book
class BookUpdate(BaseModel):
    book_title: Optional[str] = None
    book_type: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    book_price: Optional[float] = None