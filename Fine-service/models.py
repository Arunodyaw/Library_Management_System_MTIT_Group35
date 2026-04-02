from pydantic import BaseModel
from datetime import date
from typing import Optional

class Fine(BaseModel):
    due_date: date
    return_date: date
    days_late: int
    fine_amount: float

class Payment(BaseModel):
    id: int
    user_id: int
    amount: float
    payment_date: date
    status: str  # paid / pending

class PaymentCreate(BaseModel):
    user_id: int
    amount: float
    payment_date: date
    status: str  # paid / pending