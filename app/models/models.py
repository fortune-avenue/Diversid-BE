from sqlalchemy import Column, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True)
    mobile_no = Column(String(255), nullable=True, unique=True)
    full_name = Column(String(255), nullable=False, unique=False) 
    password_hash = Column(String(255), nullable=False)
    ktp_photo = Column(String, nullable=True)
    slf_ktp_photo = Column(String, nullable=True)
    email_verified = Column(Boolean, nullable=True, default=False)
    phone_verified = Column(Boolean, nullable=True, default=False)
    created_at = Column(TIMESTAMP, nullable=True, default=datetime.utcnow)

class VoiceData(Base):
    __tablename__ = "voice_data"
    
    voice_data_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    voice_file_1 = Column(String, nullable=True)
    voice_file_2 = Column(String, nullable=True)
    voice_file_3 = Column(String, nullable=True)
    voice_file_4 = Column(String, nullable=True)

class Token(Base):
    __tablename__ = "jwt_token"

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'), primary_key=True, nullable=False)
    access_token = Column(String, nullable=False) 
    token_type = Column(String, nullable=False) 