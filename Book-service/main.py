# book-service/main.py
from fastapi import FastAPI, HTTPException, status
from typing import List
from models import Book, BookCreate, BookUpdate
from service import BookService

app = FastAPI(title="Book Microservice", version="1.0.0")

# Initialize service
book_service = BookService()

@app.get("/")
def read_root():
    return {"message": "Book Microservice is running"}

# Get all books
@app.get("/books", response_model=List[Book])
def get_all_books():
    return book_service.get_all()

# Get a book by ID
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = book_service.get_by_id(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Create a new book
@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate):
    return book_service.create(book)

# Update a book
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookUpdate):
    updated_book = book_service.update(book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

# Delete a book
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    success = book_service.delete(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None