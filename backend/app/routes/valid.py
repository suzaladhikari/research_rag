import json 
from fastapi import HTTPException, UploadFile
from pypdf import PdfReader
from pathlib import Path
from io import BytesIO

### Criterias
MAX_FILE_SIZE = 10 * 1024 * 1024 ## 10 MB 
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".json"}

async def validate_file(file:UploadFile)->bytes:
    extension = Path(file.filename or "").suffix.lower() ## Getting the type of file in the lower format to check if the file matches the criteria 
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, 'Only TXT, PDF, and JSON files are allowed')
    
    ## Checking if the content has some data, filesize aand many more
    content = await file.read(MAX_FILE_SIZE+1) ## Reading the file 
    if not content:
        raise HTTPException(400, "File is empty!") ## If the file is found to be empty 
    if len(content) >= MAX_FILE_SIZE:
        raise HTTPException(413, "File exceeds the 10 MB limit")

    try: 
        if extension == '.pdf':
            if not content.startswith(b"%PDF-"): ## Usually the first line of the pdf file starts with %PDF so if not the starting with %PDF then we wont accept it 
                raise ValueError("Missing PDF header")
            reader = PdfReader(BytesIO)
            if reader.is_encrypted:
                raise ValueError("This pdf is passeword-protected PDF")

            if len(reader.pages) == 0:
                raise.ValueError("PDF has no pages")

