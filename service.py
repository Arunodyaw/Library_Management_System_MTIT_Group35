from data_service import NotificationMockDataService

class NotificationService:
    def __init__(self):
        self.data_service = NotificationMockDataService()

    def get_all(self):
        return self.data_service.get_all_notifications()
    
    def get_by_id(self, notification_id):
        return self.data_service.get_notification_by_id(notification_id)
    
    def get_by_type(self, type):    
        return self.data_service.get_notifications_by_type(type)
    
    def get_by_status(self, status):
        return self.data_service.get_notifications_by_status(status)

    def create(self, data):
        return self.data_service.add_notification(data)

    def update(self, notification_id, data):
        return self.data_service.update_notification(notification_id, data)

    def delete(self, notification_id):
        return self.data_service.delete_notification(notification_id)