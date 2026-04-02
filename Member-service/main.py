from fastapi import FastAPI, HTTPException, status
from models import Member, MemberCreate, MemberUpdate
from service import MemberService
from typing import List

app = FastAPI(title="Member Service")

service = MemberService()

@app.get("/members", response_model=List[Member])
def get_members():
    return service.get_all()


@app.get("/members/{member_id}", response_model=Member)
def get_member(member_id: int):
    member = service.get_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@app.post("/members", response_model=Member, status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreate):
    return service.create(member)

@app.put("/members/{member_id}", response_model=Member)
def update_member(member_id: int, member: MemberUpdate):
    updated = service.update(member_id, member)
    if not updated:
        raise HTTPException(status_code=404, detail="Member not found")
    return updated

@app.delete("/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int):
    success = service.delete(member_id)
    if not success:
        raise HTTPException(status_code=404, detail="Member not found")