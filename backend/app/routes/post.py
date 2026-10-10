from fastapi import APIRouter, UploadFile, HTTPException
from backend.app.routes.valid import validate_file
import boto3
import uuid
import os 
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import numpy as np
from botocore.exceptions import ClientError
from pydantic import BaseModel, Field
import psycopg2
from pgvector.psycopg2 import register_vector

load_dotenv()
router = APIRouter()
BUCKET_NAME = os.getenv("BUCKET_NAME")
## Creating the connection to the database 
connection = psycopg2.connect(os.getenv("DATABASE_URL")) ## Connecting with the database
register_vector(connection) ##The connection now accepts the column with the vecor format as well

## S3 client 
s3 = boto3.client("s3") ## Createing the boto3 client for the s3 bucket 
@router.post('/posting_router', status_code=202)
async def posting_router(file:UploadFile):
    content, content_type = await validate_file(file)
    ## Stripping away the path just to get the file name 
    file_name = os.path.basename(file.filename)
    file_id = str(uuid.uuid4())
    key = f'uploads/{file_id}/{file_name}'

    ## First uploading the file to the database 
    try:
        with connection.cursor() as cur: 
            cur.executemany("""
                INSERT INTO documents (file_id, file_name, status)
                VALUES (%s, %s, %s) 
                """, 
                uploads)
            connection.commit()
    except Exception:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail = "File has been uploaded to S3, but saving the document failed "
        )
    ### Uploading in the s3 now ! 
    try: 
        s3.put_object(
            Bucket = BUCKET_NAME, 
            Key = key, 
            Body = content, 
            ContentType = content_type
        )

    except ClientError as c:
        raise HTTPException(status_code=500, detail = f"S3 upload failed: {c}")

    ## Uploading to the table 
    uploads = [(id_file, name_file, "Uploaded") for i, (id_file, name_file) in enumerate(zip(file_id, file_name))]

    return {f"The file has been saved to {file_name}"}


### Creating the sentence transformer model 
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
def vectorize_question(text: str) ->list[float]: ## Each vector will be the size of 384 
    return sentence_model.encode(text).tolist()

### Creating the pydantic base model 
class QuestionStatus(BaseModel):
    question: str = Field(min_length=5, max_length = 1000)


@router.post('/posting_question_vector', status_code=202)
def posting_question_vector(question: QuestionStatus):
    vectors = vectorize_question(question.question) ## Question is embedded as one piece
    with connection.cursor() as cur: 
        cur.execute("""
            SELECT file_id, chunk_index, chunks, 1 - (embedding <=> %s::vector) AS similarity
            FROM chunks 
            ORDER BY embedding <=> %s::vector
            LIMIT 5 
    """, (vectors, vectors))
        rows = cur.fetchall() ## 5 differnt list of tuples will be created

    return {"results" : [
        {"file_id" : r[0], "chunk_index" : r[1], "text": r[2], "similarity": float(r[3])} for r in rows
    ]    } ## Returns the dictionary of the top 5 similar chunks 
    
### Getting the documents: 



    

