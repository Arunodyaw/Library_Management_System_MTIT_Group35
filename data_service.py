from models import Notification

class NotificationMockDataService:
    def __init__(self):
        self.notifications = []
        self.next_id = 1

    def get_all_notifications(self):
        return self.notifications

    def add_notification(self, data):
        new_notification = Notification(
            id=self.next_id,
            status="sent",
            **data.dict()
        )
        self.notifications.append(new_notification)
        self.next_id += 1
        return new_notification

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