from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    email: Optional[EmailStr]
    full_name: Optional[str]
    ktp_photo: Optional[str]  # Assuming fileid as a string for simplicity
    slf_ktp_photo: Optional[str]  # Assuming fileid as a string for simplicity
    phone_verified: Optional[bool]
    password_hash: Optional[str]

class User(BaseModel):
    user_id: uuid.UUID
    email: Optional[EmailStr]
    full_name: Optional[str]
    ktp_photo: Optional[str]  # Assuming fileid as a string for simplicity
    slf_ktp_photo: Optional[str]  # Assuming fileid as a string for simplicity
    phone_verified: Optional[bool]
    password_hash: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
