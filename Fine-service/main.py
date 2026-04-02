from fastapi import FastAPI, HTTPException, status
from models import Fine, Payment, PaymentCreate
from service import FinePaymentService
from typing import List

app = FastAPI(title="Fine & Payment Service")

service = FinePaymentService()

#  Calculate Fine
@app.post("/fine/calculate", response_model=Fine)
def calculate_fine(due_date: str, return_date: str):
    return service.calculate_fine(due_date, return_date)

@app.get("/fine/{member_id}", response_model=Fine)
def get_fine(member_id: int):
    fine = service.get_fine(member_id)
    if not fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    return fine


#  Make Payment
@app.post("/payment", response_model=Payment, status_code=status.HTTP_201_CREATED)
def make_payment(payment: PaymentCreate):
    return service.make_payment(payment)


#  Get Payment History
@app.get("/payments", response_model=List[Payment])
def get_payments():
    return service.get_payments()

@app.get("/payment/{payment_id}", response_model=Payment)
def get_payment(payment_id: int):
    payment = service.get_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.put("/payment/{payment_id}", response_model=Payment)
def update_payment(payment_id: int, payment: PaymentCreate):
    updated = service.update_payment(payment_id, payment)
    if not updated:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated

@app.delete("/payment/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment(payment_id: int):
    success = service.delete_payment(payment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Payment not found")
    return None   
 