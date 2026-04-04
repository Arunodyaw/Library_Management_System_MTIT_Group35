from models import Reservation
from datetime import date

class ReservationMockDataService:
    def __init__(self):
        self.reservations = [
            Reservation(id=1, user_id=2, book_id=2, reservation_date=date(2024, 3, 1), status="active"),
            Reservation(id=2, user_id=1, book_id=3, reservation_date=date(2024, 3, 2), status="cancelled")
        ]
        self.next_id = 3

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