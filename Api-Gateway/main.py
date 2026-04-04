from datetime import datetime,date, time
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
import httpx
from pydantic import BaseModel
from typing import Optional, Any
from datetime import date
import json  # Added for custom JSON serialization

app = FastAPI(title="Library Management API Gateway", version="1.0.0")

# 🔗 Service URLs
SERVICES = {
    "book": "http://localhost:8001",
    "borrow": "http://localhost:8002",
    "member": "http://localhost:8003",
    "payment": "http://localhost:8004",
    "reservation": "http://localhost:8005",
    "notification": "http://localhost:8006"
}

# 🔁 Forward Request Function - Fixed for date serialization
async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    url = f"{SERVICES[service]}{path}"
    
    # Handle JSON serialization for date objects
    if 'json' in kwargs:
        # Convert date objects to ISO format strings
        def convert_dates(obj):
            if isinstance(obj, date):
                return obj.isoformat()
            return obj
        
        # Apply conversion recursively
        kwargs['json'] = json.loads(
            json.dumps(kwargs['json'], default=convert_dates)
        )

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.request(method, url, **kwargs)
            
            # Handle empty responses
            content = None
            if response.text:
                try:
                    content = response.json()
                except:
                    content = response.text
            
            return JSONResponse(
                content=content,
                status_code=response.status_code
            )

        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail="Gateway timeout")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")


# ================= ROOT =================
@app.get("/")
def read_root():
    return {
        "message": "Library API Gateway is running",
        "services": list(SERVICES.keys())
    }


# ================= BOOK SERVICE =================
class Book(BaseModel):
    id: int
    book_title: str
    book_type: str
    author: str
    isbn: str
    publisher: str
    book_price: float

@app.get("/gateway/books")
async def get_books():
    return await forward_request("book", "/books", "GET")

@app.post("/gateway/books")
async def create_book(book: Book):
    return await forward_request("book", "/books", "POST", json=book.dict())

@app.get("/gateway/books/{book_id}")
async def get_book(book_id: int):    
    return await forward_request("book", f"/books/{book_id}", "GET")

@app.put("/gateway/books/{book_id}")
async def update_book(book_id: int, book: Book): 
    return await forward_request("book", f"/books/{book_id}", "PUT", json=book.dict())

@app.delete("/gateway/books/{book_id}")
async def delete_book(book_id: int):
    return await forward_request("book", f"/books/{book_id}", "DELETE")    


# ================= MEMBER SERVICE =================
class Member(BaseModel):
    id: int
    name: str
    email: str
    address: str
    phone: str

@app.get("/gateway/members")
async def get_members():
    return await forward_request("member", "/members", "GET")

@app.get("/gateway/members/{member_id}")
async def get_member(member_id: int):
    return await forward_request("member", f"/members/{member_id}", "GET")

@app.post("/gateway/members")
async def create_member(member: Member):
    return await forward_request("member", "/members", "POST", json=member.dict())

@app.put("/gateway/members/{member_id}")
async def update_member(member_id: int, member: Member):
    return await forward_request("member", f"/members/{member_id}", "PUT", json=member.dict())

@app.delete("/gateway/members/{member_id}")
async def delete_member(member_id: int):
    return await forward_request("member", f"/members/{member_id}", "DELETE")


# ================= BORROW SERVICE =================
class BorrowRecord(BaseModel):
    member_id: int
    book_id: int
    borrow_date: date
    return_date: date
    status: str="borrowed"  # borrowed / returned

class BorrowRecordUpdate(BaseModel):
    member_id: int
    book_id: int
    borrow_date: date
    return_date: date
    status: str="borrowed"  # borrowed / returned

@app.get("/gateway/borrowed-books")
async def get_borrowed_books():
    return await forward_request("borrow", "/borrowed-books", "GET")

@app.post("/gateway/borrow")
async def borrow_book(record: BorrowRecord): 
    return await forward_request("borrow", "/borrow", "POST", json=record.dict())   

@app.get("/gateway/borrow/{record_id}")
async def get_borrow_record(record_id: int):
    return await forward_request("borrow", f"/borrow/{record_id}", "GET")

@app.put("/gateway/borrow/{record_id}")
async def update_borrow_record(record_id: int, record: BorrowRecordUpdate):
    return await forward_request("borrow", f"/borrow/{record_id}", "PUT", json=record.dict())   

@app.delete("/gateway/borrow/{record_id}")
async def delete_borrow_record(record_id: int):
    return await forward_request("borrow", f"/borrow/{record_id}", "DELETE")


# ================= PAYMENT SERVICE =================
class Payment(BaseModel):
    user_id: int
    amount: float
    payment_date: date
    status: str="paid" # paid / pending



@app.post("/gateway/payment")
async def make_payment(payment: Payment):
    # Convert date to string before sending
    payment_dict = payment.dict()
    payment_dict['payment_date'] = payment_dict['payment_date'].isoformat()
    return await forward_request("payment", "/payment", "POST", json=payment_dict)

@app.get("/gateway/payments")
async def get_payments():
    return await forward_request("payment", "/payments", "GET")

# Fine Model
class Fine(BaseModel):
    due_date: date
    return_date: date
    days_late: int = 0
    fine_amount: float = 0.0

# Direct calculation without calling payment service (if payment service doesn't have the endpoint)
@app.post("/gateway/fine/calculate")
async def calculate_fine(
    due_date: str = Query(..., description="Due date (YYYY-MM-DD)"),
    return_date: str = Query(..., description="Return date (YYYY-MM-DD)")
):
    """
    Calculate fine based on due date and return date
    Fine rate: Rs:25/= per day late
    """
    try:
        # Parse dates
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d").date()
        return_date_obj = datetime.strptime(return_date, "%Y-%m-%d").date()
        
        # Validate dates
        if return_date_obj < due_date_obj:
            return JSONResponse(
                content={
                    "success": False,
                    "message": "Return date cannot be before due date",
                    "due_date": due_date,
                    "return_date": return_date,
                    "days_late": 0,
                    "fine_amount": 0.0
                },
                status_code=400
            )
        
        # Calculate fine
        days_late = (return_date_obj - due_date_obj).days
        fine_rate_per_day = 25  # $25 per day
        fine_amount = days_late * fine_rate_per_day
        
        # Create response
        result = {
            "success": True,
            "due_date": due_date,
            "return_date": return_date,
            "days_late": days_late,
            "fine_amount": fine_amount,
            "fine_rate_per_day": fine_rate_per_day,
            "message": f"Fine calculated: Rs: {fine_amount:.2f} for {days_late} day(s) late"
        }
        
        # Try to forward to payment service if available
        try:
            fine = Fine(
                due_date=due_date_obj,
                return_date=return_date_obj,
                days_late=days_late,
                fine_amount=fine_amount
            )
            
            fine_dict = fine.dict()
            fine_dict['due_date'] = fine_dict['due_date'].isoformat()
            fine_dict['return_date'] = fine_dict['return_date'].isoformat()
            
            # Uncomment if payment service has this endpoint
            # return await forward_request("payment", "/fine/calculate", "POST", json=fine_dict)
            
            # For now, return calculated result directly
            return JSONResponse(content=result, status_code=200)
            
        except Exception as e:
            # If payment service fails, still return calculated result
            result["warning"] = f"Payment service unavailable: {str(e)}"
            return JSONResponse(content=result, status_code=200)
        
    except ValueError as e:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid date format: {str(e)}. Please use YYYY-MM-DD format (e.g., 2026-04-05)"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating fine: {str(e)}")

# Alternative: Accept dates in request body
class FineRequest(BaseModel):
    due_date: str
    return_date: str


    
@app.get("/gateway/payment/{payment_id}")
async def get_payment(payment_id: int):
    return await forward_request("payment", f"/payment/{payment_id}", "GET")


@app.put("/gateway/payment/{payment_id}")
async def update_payment(payment_id: int, payment: Payment):
    # Convert date to string before sending
    payment_dict = payment.dict()
    payment_dict['payment_date'] = payment_dict['payment_date'].isoformat()
    return await forward_request("payment", f"/payment/{payment_id}", "PUT", json=payment_dict)

@app.delete("/gateway/payment/{payment_id}")
async def delete_payment(payment_id: int):
    return await forward_request("payment", f"/payment/{payment_id}", "DELETE")


# ================= RESERVATION SERVICE =================
class Reservation(BaseModel):

    
    user_id: int
    book_id: int
    reservation_date: date
    status: str="active"  # active / cancelled

class ReservationUpdate(BaseModel):
    user_id: int
    book_id: int
    reservation_date: date
    status: str="active"  # active / cancelled

@app.get("/gateway/reservations")
async def get_reservations():
    return await forward_request("reservation", "/reservations", "GET")

@app.get("/gateway/reservations/{reservation_id}")
async def get_reservation(reservation_id: int):
    return await forward_request("reservation", f"/reservations/{reservation_id}", "GET")

@app.post("/gateway/reservations")
async def add_reservation(reservation: Reservation):
    # Convert date to string before sending
    reservation_dict = reservation.dict()
    reservation_dict['reservation_date'] = reservation_dict['reservation_date'].isoformat()
    return await forward_request("reservation", "/reservations", "POST", json=reservation_dict)

@app.put("/gateway/reservations/{reservation_id}")
async def update_reservation(reservation_id: int, reservation: ReservationUpdate):
    # Convert date to string before sending
    reservation_dict = reservation.dict()
    reservation_dict['reservation_date'] = reservation_dict['reservation_date'].isoformat()
    return await forward_request("reservation", f"/reservations/{reservation_id}", "PUT", json=reservation_dict)

@app.delete("/gateway/reservations/{reservation_id}")
async def delete_reservation(reservation_id: int):
    return await forward_request("reservation", f"/reservations/{reservation_id}", "DELETE")




# ================= NOTIFICATION SERVICE =================
class Notification(BaseModel):
    user_id: int
    notification_date: date
    notification_time: time
    message: str
    type: str = "return reminder"  # reminder / reservation / payment
    status: str = "pending"  # sent / pending


@app.get("/gateway/notifications")
async def get_notifications():
    return await forward_request("notification", "/notifications", "GET")

@app.get("/gateway/notifications/{notification_id}")
async def get_notification(notification_id: int):
    return await forward_request("notification", f"/notifications/{notification_id}", "GET")

@app.get("/gateway/notifications/type/{type}")
async def get_notifications_by_type(type: str):
    return await forward_request("notification", f"/notifications/type/{type}", "GET")

@app.get("/gateway/notifications/status/{status}")
async def get_notifications_by_status(status: str):
    return await forward_request("notification", f"/notifications/status/{status}", "GET")

@app.post("/gateway/notifications")
async def add_notification(notification: Notification):
    # Convert date and time to string before sending
    notification_dict = notification.dict()
    notification_dict['notification_date'] = notification_dict['notification_date'].isoformat()
    notification_dict['notification_time'] = notification_dict['notification_time'].isoformat()
    return await forward_request("notification", "/notifications", "POST", json=notification_dict)  


@app.put("/gateway/notifications/{notification_id}")
async def update_notification(notification_id: int, notification: Notification):
    # Convert date and time to string before sending
    notification_dict = notification.dict()
    notification_dict['notification_date'] = notification_dict['notification_date'].isoformat()
    notification_dict['notification_time'] = notification_dict['notification_time'].isoformat()
    return await forward_request("notification", f"/notifications/{notification_id}", "PUT", json=notification_dict)

@app.delete("/gateway/notifications/{notification_id}")
async def delete_notification(notification_id: int):
    # Fixed: Removed trailing comma
    return await forward_request("notification", f"/notifications/{notification_id}", "DELETE")