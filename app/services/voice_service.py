from sqlalchemy.orm import Session
from app.models.models import VoiceData
from app.schemas.schemas import VoiceDataCreate
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os
import uuid
from resemblyzer import VoiceEncoder, preprocess_wav
from scipy.spatial.distance import cosine
from pydub import AudioSegment
from fastapi import UploadFile

# Ensure GOOGLE_APPLICATION_CREDENTIALS is set
if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json')
encoder = VoiceEncoder()

def create_voice_data(db: Session, voice_data: VoiceDataCreate):
    db_voice_data = VoiceData(**voice_data.dict())
    db.add(db_voice_data)
    db.commit()
    db.refresh(db_voice_data)
    return db_voice_data

def upload_to_gcs(file_path: str, bucket_name: str, destination_blob_name: str):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(file_path)
    return blob.public_url

def convert_to_wav(uploaded_file: UploadFile):
    temp_m4a_file = f"/tmp/{uuid.uuid4()}.m4a"
    temp_wav_file = f"/tmp/{uuid.uuid4()}.wav"

    with open(temp_m4a_file, "wb") as f:
        f.write(uploaded_file.file.read())

    audio = AudioSegment.from_file(temp_m4a_file, format="m4a")
    audio.export(temp_wav_file, format="wav")

    return temp_wav_file

def download_file_from_gcs(bucket_name, source_blob_name, destination_file_name):
    source_blob_name = source_blob_name.replace("%2F", "/")
    destination_file_name = destination_file_name.replace("%2F", "/")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    if not blob.exists():
        raise Exception(f"File {source_blob_name} does not exist in bucket {bucket_name}")
    print(destination_file_name)
    blob.download_to_filename(destination_file_name)
    return destination_file_name

def compare_voice_with_user_files(user_id, uploaded_file, db: Session, bucket_name, similarity_threshold=0.7):
    temp_file = f"/tmp/{uuid.uuid4()}_{uploaded_file.filename}"
    
    # Save the uploaded file temporarily
    with open(temp_file, "wb") as f:
        f.write(uploaded_file.file.read())
    
    uploaded_wav = preprocess_wav(temp_file)
    uploaded_embedding = encoder.embed_utterance(uploaded_wav)
    
    user_voice_data = db.query(VoiceData).filter(VoiceData.user_id == user_id).first()
    if not user_voice_data:
        raise Exception("User voice data not found")
    
    for voice_file in [user_voice_data.voice_file_1, user_voice_data.voice_file_2, user_voice_data.voice_file_3, user_voice_data.voice_file_4]:
        if voice_file:
            voice_file_name = voice_file.split('/')[-1]
            local_voice_file = f"/tmp/{voice_file_name}"
            download_file_from_gcs(bucket_name, voice_file_name, local_voice_file)
            
            wav = preprocess_wav(local_voice_file)
            embedding = encoder.embed_utterance(wav)
            
            similarity = 1 - cosine(uploaded_embedding, embedding)
            if similarity >= similarity_threshold:
                os.remove(temp_file)
                os.remove(local_voice_file)
                return True
    
    os.remove(temp_file)
    return False