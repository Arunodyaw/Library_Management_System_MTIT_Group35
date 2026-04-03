from models import Notification
from datetime import datetime, timedelta
from typing import List, Dict
from enum import Enum

class NotificationMockDataService:
    def __init__(self):
        self.notifications = []
        self.next_id = 1

    def get_all_notifications(self):
        return self.notifications

    def add_notification(self, data):
        notification = Notification(
            id=self.next_id,
            user_id=data.user_id,
            notification_date=data.notification_date,
            notification_time=data.notification_time,
            message=data.message,
            type=data.type,
            status=data.status
        )
        self.notifications.append(notification)
        self.next_id += 1
        return notification
    
    def get_notification_by_id(self, notification_id:int):
        for n in self.notifications:
            if n.id == notification_id:
                return n
        return None
    
    def get_notifications_by_type(self, type:str):
        return [n for n in self.notifications if n.type == type]
    
    def get_notifications_by_status(self, status:str):
        return [n for n in self.notifications if n.status == status]

    def update_notification(self, notification_id, data):
        for n in self.notifications:
            if n.id == notification_id:
                update_data = data.dict(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(n, key, value)
                return n
        return None

    def delete_notification(self, notification_id):
        for n in self.notifications:
            if n.id == notification_id:
                self.notifications.remove(n)
                return True
        return False