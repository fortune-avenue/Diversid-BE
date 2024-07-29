import cv2
import os
import numpy as np
from ultralytics import YOLO
from PIL import Image
import tempfile

# Load YOLO model
model = YOLO('last.pt')

def extract_faces(image_bytes):
    # Convert image bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Image could not be loaded.")
    
    # Perform face detection
    results = model(img)
    
    # Extract bounding boxes
    boxes = results[0].boxes.xyxy.cpu().numpy()  # x1, y1, x2, y2
    classes = results[0].boxes.cls.cpu().numpy()  # class
    
    extracted_faces = []
    for box, cls in zip(boxes, classes):
        if int(cls) == 0:  # Class 0 corresponds to 'person' in YOLO
            x1, y1, x2, y2 = box
            face = img[int(y1):int(y2), int(x1):int(x2)]
            extracted_faces.append(face)
    
    return extracted_faces
    