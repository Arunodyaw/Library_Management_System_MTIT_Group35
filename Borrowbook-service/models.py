from pydantic import BaseModel
from typing import Optional
from datetime import date

class BorrowRecord(BaseModel):
    id: int
    member_id: int
    book_id: int
    borrow_date: date
    return_date: date
    status: str  # borrowed / returned

class BorrowCreate(BaseModel):
    member_id: int
    book_id: int
    borrow_date: date
    return_date: date