from fastapi import APIRouter, UploadFile, File
from backend.app.routes.valid import validate_file
router = APIRouter()

@router.post('/posting_router', status_code=202)
async def posting_router(file:UploadFile):
    content = await validate_file(file)
    return {"filename": file.filename, "size": len(content), "content": content}