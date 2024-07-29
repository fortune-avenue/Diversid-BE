import cv2
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from deepface import DeepFace
from PIL import Image
from app.services.face_service import extract_faces
import io
import base64

router = APIRouter(
    prefix="/verification",
    tags=["verification"],
)
@router.post("/compare/")
async def extract_faces_endpoint(image: UploadFile = File(...)):
    try:
        # Read image bytes
        image_bytes = await image.read()
        
        # Extract faces
        faces = extract_faces(image_bytes)
        
        if len(faces) < 2:
            raise ValueError("At least two faces are required for comparison.")
        
        # Convert faces to base64 for easy transmission
        face_base64 = []
        for face in faces[:2]:  # Only process the first two faces
            face_pil = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
            buffered = io.BytesIO()
            face_pil.save(buffered, format="JPEG")
            face_base64.append(base64.b64encode(buffered.getvalue()).decode('utf-8'))
        
        # Compare the two faces using DeepFace library
        face1_array = faces[0]
        face2_array = faces[1]
        comparison_result = DeepFace.verify(face1_array, face2_array, threshold=0.70)
        
        # Return a JSON response with the result
        return JSONResponse({
            'comparison_result': {
                'verified': str(comparison_result['verified']),
                'distance': str(comparison_result['distance']),
                'threshold': str(comparison_result['threshold'])
            }
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))