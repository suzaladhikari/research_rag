from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.app.routes.valid import validate_file
from backend.app.worker import vectorize_chunks
import boto3
import uuid
import os 
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import numpy as np
from botocore.exceptions import ClientError
load_dotenv()
router = APIRouter()
BUCKET_NAME = os.getenv("BUCKET_NAME")
s3 = boto3.client("s3") ## Createing the boto3 client for the s3 bucket 
@router.post('/posting_router', status_code=202)
async def posting_router(file:UploadFile):
    content, content_type = await validate_file(file)
    ## Stripping away the path just to get the file name 
    file_name = os.path.basename(file.filename)
    key = f'uploads/{uuid.uuid4()}/{file_name}'
    try: 
        s3.put_object(
            Bucket = BUCKET_NAME, 
            Key = key, 
            Body = content, 
            ContentType = content_type
        )
    except ClientError as c:
        raise HTTPException(status_code=500, detail = f"S3 upload failed: {c}")

    return {f"The file has been saved to {file_name}"}
### Creating the sentence transformer model 

sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
def vectorize_question(text: str) ->list[list[float]]: ## Each vector will be the size of 384 
    return sentence_model.encode(text).toist()
@router.post('/posting_question_vector', status_code=202)
def posting_question_vector(question: str):
    vectors = vectorize_question(question) ## Question is embedded as one piece
    return vectors
    


    

