from data_service import ReservationMockDataService

class ReservationService:
    def __init__(self):
        self.data_service = ReservationMockDataService()

    def get_all(self):
        return self.data_service.get_all()
    
    def get_by_id(self, reservation_id):
        return self.data_service.get_reservation_by_id(reservation_id)

    def create(self, data):
        return self.data_service.add_reservation(data)
    
    def update(self, reservation_id, data):
        return self.data_service.update_reservation(reservation_id, data)

    def cancel(self, reservation_id):
        return self.data_service.delete_reservation(reservation_id)