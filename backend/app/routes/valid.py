import json 
from fastapi import HTTPException, UploadFile
from pypdf import PdfReader
from pathlib import Path

### Criterias
MAX_FILE_SIZE = 10 * 1024 * 1024 ## 10 MB 
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".json"}

async def validate_file(file:UploadFile)->bytes:
    extension = Path(file.filename or "").suffix.lower() ## Getting the type of file in the lower format to check if the file matches the criteria 

    