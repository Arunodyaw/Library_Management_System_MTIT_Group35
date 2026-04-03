from fastapi import FastAPI, HTTPException, status
from models import Reservation, ReservationCreate
from service import ReservationService
from typing import List

app = FastAPI(title="Reservation Service")

service = ReservationService()

# ✅ GET all reservations
@app.get("/reservations", response_model=List[Reservation])
def get_reservations():
    return service.get_all()

@app.get("/reservations/{reservation_id}", response_model=Reservation)
def get_reservation(reservation_id: int):    
    reservation = service.get_by_id(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

# ✅ POST reserve a book
@app.post("/reservations", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def reserve_book(data: ReservationCreate):
    return service.create(data)

@app.put("/reservations/{reservation_id}", response_model=Reservation)
def update_reservation(reservation_id: int, data: ReservationCreate):
    reservation = service.update(reservation_id, data)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

# ✅ DELETE cancel reservation
@app.delete("/reservations/{reservation_id}", response_model=Reservation)
def cancel_reservation(reservation_id: int):
    reservation = service.cancel(reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation