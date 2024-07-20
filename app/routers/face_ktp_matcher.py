from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from deepface import DeepFace
import numpy as np
from PIL import Image
import io

router = APIRouter(
    prefix="/verification",
    tags=["verification"],
)

@router.post("/compare-faces/")
async def compare_faces(image1: UploadFile = File(...), image2: UploadFile = File(...)):
    try:
        # Load the uploaded images using Pillow
        image1 = Image.open(io.BytesIO(await image1.read())).convert('RGB')
        image2 = Image.open(io.BytesIO(await image2.read())).convert('RGB')

        # Convert images to numpy arrays
        image1_array = np.array(image1)
        image2_array = np.array(image2)

        # Compare the two images using DeepFace library
        result = DeepFace.verify(image1_array, image2_array, threshold=0.70)

        # Return a JSON response with the result
        return JSONResponse(
            {'result': str(result['verified']),
             'distance': str(result['distance']),
             'threshold': str(result['threshold'])}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
