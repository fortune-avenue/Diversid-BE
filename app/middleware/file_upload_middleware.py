from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from fastapi import UploadFile
import os
import shutil

class FileUploadMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/upload-file" and request.method == "POST":
            form = await request.form()
            file: UploadFile = form["file"]
            
            # Save the uploaded file to a directory
            upload_dir = "cache"
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, file.filename)
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            response = Response(f"File {file.filename} uploaded successfully!")
        else:
            response = await call_next(request)
        
        return response
