from fastapi import FastAPI, HTTPException
from models import BorrowRecord, BorrowCreate
from service import BorrowService
from typing import List

app = FastAPI(title="Borrow Service")

service = BorrowService()

#  Borrow Book
@app.post("/borrow", response_model=BorrowRecord)
def borrow_book(data: BorrowCreate):
    return service.borrow(data)

@app.get("/borrow/{record_id}", response_model=BorrowRecord)
def get_borrow_record(record_id: int):
    record = service.get_by_id(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record
    

#  View Borrowed Books
@app.get("/borrowed-books", response_model=List[BorrowRecord])
def get_records():
    return service.get_all()

@app.put("/borrow/{record_id}", response_model=BorrowRecord)
def update_borrow_record(record_id: int, data: BorrowCreate):
    updated = service.update(record_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Record not found")
    return updated

@app.delete("/borrow/{record_id}", status_code=204)
def delete_borrow_record(record_id: int):
    success = service.delete(record_id)
    if not success:
        raise HTTPException(status_code=404, detail="Record not found")
    return None