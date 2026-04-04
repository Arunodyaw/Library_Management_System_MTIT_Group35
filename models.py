from datetime import date, time

from pydantic import BaseModel
from typing import Optional

class Notification(BaseModel):
    id: int
    user_id: int
    notification_date: date
    notification_time: time
    message: str
    type: str = "return reminder"  # reminder / reservation / payment
    status: str = "pending"  # sent / pending

class NotificationCreate(BaseModel):
    user_id: int
    notification_date: date
    notification_time: time
    message: str
    type: str = "return reminder"
    status: str = "pending"

class NotificationUpdate(BaseModel):
    user_id: Optional[int]
    notification_date: Optional[date]
    notification_time: Optional[time]
    message: Optional[str]
    type: Optional[str]  # reminder / reservation / payment
    status: Optional[str]  # sent / pending