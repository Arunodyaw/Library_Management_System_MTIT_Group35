from pydantic import BaseModel
from datetime import date
from typing import Optional

class Reservation(BaseModel):
    id: int
    user_id: int
    book_id: int
    reservation_date: date
    status: str  # active / cancelled

class ReservationCreate(BaseModel):
    user_id: int
    book_id: int
    reservation_date: date
    status: str = "active"  # active / cancelled

class ReservationUpdate(BaseModel):
    user_id: int
    book_id: int
    reservation_date: date
    status: str = "active"  # active / cancelled