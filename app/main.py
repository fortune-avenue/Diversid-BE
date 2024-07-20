from fastapi import FastAPI
from database import Base, engine
from routers import user, face_ktp_matcher
from middleware.file_upload_middleware import FileUploadMiddleware

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(FileUploadMiddleware)

app.include_router(user.router)
app.include_router(face_ktp_matcher.router)