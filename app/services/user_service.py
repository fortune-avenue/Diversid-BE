from sqlalchemy.orm import Session
from app.models.models import User
from app.schemas.schemas import UserCreate
import uuid
from datetime import datetime
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict(), created_at=datetime.utcnow())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: uuid.UUID):
    return db.query(User).filter(User.user_id == user_id).first()

def update_user(db: Session, user_id: uuid.UUID, user: UserCreate):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        for key, value in user.dict().items():
            if value is not None:
                setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: uuid.UUID):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user and pwd_context.verify(password, db_user.password_hash):
        return db_user
    return None