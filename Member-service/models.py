from pydantic import BaseModel
from typing import Optional

class Member(BaseModel):
    id: int
    name: str
    email: str
    address: str
    phone: str

class MemberCreate(BaseModel):
    name: str
    email: str
    address: str
    phone: str

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None