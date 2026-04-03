from models import Reservation
from datetime import date

class ReservationMockDataService:
    def __init__(self):
        self.reservations = []
        self.next_id = 1

    def get_all(self):
        return self.reservations
    
    def get_reservation_by_id(self, reservation_id):
        return next((r for r in self.reservations if r.id == reservation_id), None) 

    def add_reservation(self, data):
        reservation = Reservation(
            id=self.next_id,
            user_id=data.user_id,
            book_id=data.book_id,
            reservation_date=date.today(),
            status="active"
        )
        self.reservations.append(reservation)
        self.next_id += 1
        return reservation

    def delete_reservation(self, reservation_id):
        for r in self.reservations:
            if r.id == reservation_id:
                r.status = "cancelled"
                return r
        return None