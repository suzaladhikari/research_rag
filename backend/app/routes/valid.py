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
    if extension not in ALLOWED_EXTENSIONS: ## Immediately rejecting the file that are not in the allowed extensions
        raise HTTPException(400, 'Only TXT, PDF, and JSON files are allowed')
    
    ## Checking if the content has some data, filesize aand many more
    content = await file.read(MAX_FILE_SIZE+1) ## Reading the file 
    if not content: ## If there is nothing in the content
        raise HTTPException(400, "File is empty!") ## If the file is found to be empty 
    if len(content) >= MAX_FILE_SIZE: ## If the size of file is not good
        raise HTTPException(413, "File exceeds the 10 MB limit")

    try: 
        if extension == '.pdf':
            if not content.startswith(b"%PDF-"): ## Usually the first line of the pdf file starts with %PDF so if not the starting with %PDF then we wont accept it 
                raise ValueError("Missing PDF header")
            reader = PdfReader(BytesIO(content))
            if reader.is_encrypted:
                raise ValueError("This pdf is passeword-protected PDF")

            if len(reader.pages) == 0:
                raise ValueError("PDF has no pages")
            if not any((page.extract_text() or "").strip() for page in reader.pages): ## If any pdf from the pages has no extractable text then return that there is no such thing
                raise ValueError("Pdf has no extractable text")
        else:
            decoded = content.decode('utf-8-sig')
            if extension == '.json':
                data = json.loads(decoded)
                if data == {} or data == []:
                    raise ValueError("The file is empty")
            else:
                if not decoded.strip():
                    raise ValueError("Text file has no content")
    except (ValueError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HTTPException(400, f"Invalid {extension} file: {exc}") from exc 

    except Exception as exc:
        if extension == ".pdf":
            raise HTTPException(400, "PDF could not be read") from exc
        raise

    return content 

