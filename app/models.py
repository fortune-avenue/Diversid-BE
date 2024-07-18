from sqlalchemy import Column, String, Boolean, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=True)
    ktp_photo = Column(String, nullable=True)  # Assuming fileid as a string for simplicity
    slf_ktp_photo = Column(String, nullable=True)  # Assuming fileid as a string for simplicity
    phone_verified = Column(Boolean, nullable=True)
    password_hash = Column(String(20), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
