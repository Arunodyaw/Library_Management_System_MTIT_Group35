from fastapi import FastAPI, HTTPException, status
from models import Notification, NotificationCreate, NotificationUpdate
from service import NotificationService
from typing import List

app = FastAPI(title="Notification Service", version="1.0.0")

service = NotificationService()

@app.get("/")
def root():
    return {"message": "Notification Service Running"}

# ✅ GET all notifications
@app.get("/notifications", response_model=List[Notification])
def get_notifications():
    return service.get_all()

# ✅ POST send notification
@app.post("/notify", response_model=Notification, status_code=status.HTTP_201_CREATED)
def send_notification(notification: NotificationCreate):
    return service.create(notification)

# ✅ UPDATE notification
@app.put("/notifications/{notification_id}", response_model=Notification)
def update_notification(notification_id: int, notification: NotificationUpdate):
    updated = service.update(notification_id, notification)
    if not updated:
        raise HTTPException(status_code=404, detail="Notification not found")
    return updated

# ✅ DELETE notification
@app.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(notification_id: int):
    success = service.delete(notification_id)
    if not success:
        raise HTTPException(status_code=404, detail="Notification not found")
    return None