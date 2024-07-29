from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid

class UserCreate(BaseModel):
    email: EmailStr
    mobile_no: str
    password_hash: str
    ktp_photo: Optional[str] = None
    slf_ktp_photo: Optional[str] = None
    email_verified: Optional[bool] = None
    phone_verified: Optional[bool] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserSchema(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    mobile_no: str
    password_hash: str
    ktp_photo: Optional[str] = None
    slf_ktp_photo: Optional[str] = None
    email_verified: Optional[bool] = None
    phone_verified: Optional[bool] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class VoiceDataCreate(BaseModel):
    user_id: uuid.UUID
    voice_file_1: Optional[str] = None
    voice_file_2: Optional[str] = None
    voice_file_3: Optional[str] = None
    voice_file_4: Optional[str] = None

class VoiceDataSchema(BaseModel):
    voice_data_id: uuid.UUID
    user_id: uuid.UUID
    voice_file_1: Optional[str] = None
    voice_file_2: Optional[str] = None
    voice_file_3: Optional[str] = None
    voice_file_4: Optional[str] = None

    class Config:
        orm_mode = True
