from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.services.user_service import authenticate_user, create_user, get_user, update_user, delete_user
from app.schemas.schemas import UserCreate, UserSchema , UserLogin
import uuid
from app.db.database import Database
from passlib.context import CryptContext

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

@router.delete("/{user_id}", response_model=UserSchema)
async def delete_existing_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        db_user = delete_user(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = authenticate_user(db, user.email, user.password)
        if db_user is None:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        return {"message": "Login successful", "user_id": db_user.user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))