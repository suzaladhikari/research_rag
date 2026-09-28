from fastapi import APIRouter, UploadFile, File
from backend.app.routes.valid import validate_file
import boto3
import uuid
import os 
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
BUCKET_NAME = os.getenv("BUCKET_NAME")
s3 = boto3.client("s3") ## Createing the boto3 client for the s3 bucket 
@router.post('/posting_router', status_code=202)
async def posting_router(file:UploadFile):
    content = await validate_file(file)
    ## Stripping away the path just to get the file name 
    file_name = os.path.basename(file.filename)
    

