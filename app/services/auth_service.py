from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
from passlib.context import CryptContext
from typing import Optional
from app.models.models import User
from app.schemas.schemas import UserCreate

# JWT configuration
SECRET_KEY = "mewingrizzskibidi"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 36000

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Additional service functions
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.dict(), created_at=datetime.utcnow())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    db_user = get_user_by_email(db, email)
    if db_user and pwd_context.verify(password, db_user.password_hash):
        return db_user
    return None