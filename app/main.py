from app.db.database import Database
from fastapi import FastAPI

# Include the routes
from app.routers.user_route import router as user_router
from app.routers.voice_route import router as voice_router
from app.routers.face_ktp_matcher import router as face_router

# setup db
db = Database()
app = FastAPI()

app.include_router(user_router)
app.include_router(voice_router)
app.include_router(face_router)

