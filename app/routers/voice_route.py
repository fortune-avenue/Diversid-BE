from fastapi import Form,APIRouter, HTTPException, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.services.voice_service import convert_to_wav, compare_voice_with_user_files, create_voice_data, upload_to_gcs
from app.schemas.schemas import VoiceDataCreate, VoiceDataSchema
import uuid
import os
from app.db.database import Database

router = APIRouter(
    prefix="/voice",
    tags=["voice"],
)
database = Database()

def get_db():
    db = database.get_session()
    try:
        yield db
    finally:
        db.close()

@router.post("/create-voice", response_model=VoiceDataSchema)
async def create_voice(user_id: uuid.UUID = Form(...), 
                       voice_file_1: UploadFile = File(None), 
                       voice_file_2: UploadFile = File(None), 
                       voice_file_3: UploadFile = File(None), 
                       voice_file_4: UploadFile = File(None), 
                       db: Session = Depends(get_db)):

    try:
        bucket_name = "diversid-be"
        file_paths = []

        for file in [voice_file_1, voice_file_2, voice_file_3, voice_file_4]:
            if file:
                if file.filename.endswith(".m4a"):
                    converted_file_path = convert_to_wav(file)
                    destination_blob_name = f"{user_id}/{os.path.basename(converted_file_path)}"
                    file_path = upload_to_gcs(converted_file_path, bucket_name, destination_blob_name)
                    file_paths.append(file_path)
                    os.remove(converted_file_path)  # Remove temp file after upload
                else:
                    destination_blob_name = f"{user_id}/{file.filename}"
                    temp_file_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
                    with open(temp_file_path, "wb") as temp_file:
                        temp_file.write(file.file.read())
                    file_path = upload_to_gcs(temp_file_path, bucket_name, destination_blob_name)
                    file_paths.append(file_path)
                    os.remove(temp_file_path)  # Remove temp file after upload

        voice_data = VoiceDataCreate(
            user_id=user_id,
            voice_file_1=file_paths[0] if len(file_paths) > 0 else None,
            voice_file_2=file_paths[1] if len(file_paths) > 1 else None,
            voice_file_3=file_paths[2] if len(file_paths) > 2 else None,
            voice_file_4=file_paths[3] if len(file_paths) > 3 else None
        )
        
        return create_voice_data(db, voice_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/compare-voice")
async def compare_voice(user_id: uuid.UUID = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        bucket_name = "diversid-be"
        is_similar = compare_voice_with_user_files(user_id, file, db, bucket_name)
        return {"is_similar": is_similar}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))