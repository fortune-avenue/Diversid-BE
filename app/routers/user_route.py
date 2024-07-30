from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.user_service import authenticate_user, create_user, get_user, update_user, delete_user
from app.schemas.schemas import UserCreate, UserSchema , UserLogin, UserSignup, TokenDataSchema
import uuid
from app.db.database import Database
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.services.user_service import * 
from app.services.auth_service import *
from app.models.models import Token
import logging

router = APIRouter(
    prefix="/users",
    tags=["users"],
)
database = Database()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = database.get_session()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=UserSchema)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = pwd_context.hash(user.password_hash)
        user.password_hash = hashed_password
        return create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserSchema)
async def read_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        db_user = get_user(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{user_id}", response_model=UserSchema)
async def update_existing_user(user_id: uuid.UUID, user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = update_user(db, user_id, user)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# @router.delete("/{user_id}", response_model=UserSchema)
# async def delete_existing_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
#     try:
#         db_user = delete_user(db, user_id)
#         if db_user is None:
#             raise HTTPException(status_code=404, detail="User not found")
#         return db_user
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenDataSchema)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    logging.info(f"Received login request: {user.dict()}")
    try:
        db_user = authenticate_user(db, user.email, user.password_hash)
        if db_user is None:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(db_user.user_id)}, expires_delta=access_token_expires
        )
        return {"user_id": str(db_user.user_id), "access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/signup", response_model=TokenDataSchema)
async def signup(user: UserSignup, db: Session = Depends(get_db)):
    try:
        print("here")
        db_user = get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = pwd_context.hash(user.password)
        user_data = user.dict()
        user_data['password_hash'] = hashed_password
        new_user = create_user(db, UserCreate(**user_data))
        print(new_user.user_id)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(new_user.user_id)}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = Token(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.user_id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    return user

@router.get("/check-token")
async def check_token(current_user: User = Depends(get_current_user)):
    return {"message": "Token is valid", "user_id": current_user.user_id}