from pydantic import BaseModel
from typing import Optional

class Notification(BaseModel):
    id: int
    user_id: int
    message: str
    type: str   # reminder / reservation / payment
    status: str # sent / pending

class NotificationCreate(BaseModel):
    user_id: int
    message: str
    type: str

class NotificationUpdate(BaseModel):
    message: Optional[str] = None
    status: Optional[str] = None