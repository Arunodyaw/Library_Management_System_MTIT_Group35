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
    
    def update_reservation(self, reservation_id, data):
        reservation = self.get_reservation_by_id(reservation_id)
        if reservation:
            update_data = data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(reservation, key, value)
            return reservation
        return None

    def delete_reservation(self, reservation_id):
        reservation = self.get_reservation_by_id(reservation_id)
        if reservation:
            self.reservations.remove(reservation)
            return True
        return False