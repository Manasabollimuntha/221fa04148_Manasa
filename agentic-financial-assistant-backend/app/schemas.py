# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ParentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class ParentLogin(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str

class ReminderCreate(BaseModel):
    title: str
    message: Optional[str] = ""
    minutes_from_now: int = 0

class ReminderOut(BaseModel):
    _id: str
    parent_id: str
    title: str
    message: str
    send_at: datetime
    sent: bool
