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
            cur.execute("""
                INSERT INTO documents (file_id, file_name, status)
                VALUES (%s, %s, %s) 
                """, 
                (file_id, file_name, "uploaded"))
            connection.commit()
    except Exception:
        connection.rollback()
        raise HTTPException(
            status_code=500,
            detail = "Saving the document failed"
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
        with connection.cursor() as cur:
            cur.execute("DELETE FROM documents WHERE file_id = %s", (file_id,))
        connection.commit()
        raise HTTPException(status_code=500, detail = f"S3 upload failed: {c}")

    ## Uploading to the table 
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
            SELECT file_id, chunk_index, chunks, 1 - (embedding <=> %s::vector) AS similarity,file_name
            FROM chunks 
            ORDER BY embedding <=> %s::vector
            LIMIT 5 
    """, (vectors, vectors))
        rows = cur.fetchall() ## 5 differnt list of tuples will be created

    return {"results" : [
        {"file_id" : r[0], "chunk_index" : r[1], "text": r[2], "similarity": float(r[3]), "file_name": r[4]} for r in rows
    ]    } ## Returns the dictionary of the top 5 similar chunks 
    
### Getting the documents endpoint 
@router.get('/documents')
def documents():
    with connection.cursor() as cur: 
        cur.execute("""
        SELECT file_id, file_name, status
        from documents 
        """)
        rows = cur.fetchall()
    return [
        {"file_id":r[0], "file_name":r[1], "status":r[2]} for r in rows
    ]


## Creating the deleting statement: 
@router.delete('/documents/{file_id}')
def delete_object(file_id: str):
    ### Detecting if it is the valid file_id or not 
    try:
        uuid.UUID(file_id) ## rejecting if it is not the valid uid 
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid file id")
    with connection.cursor() as cur:
        cur.execute("SELECT file_name FROM documents WHERE file_id = %s", (file_id, ))
        row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Document not found")
    file_name = row[0]
    ### Removing the records from both chunks and database 
    try:
        with connection.cursor() as cur:
            cur.execute("DELETE FROM chunks WHERE file_id = %s", (file_id, ))
            cur.execute("DELETE FROM documents WHERE file_id = %s", (file_id, ))
            if cur.rowcount == 0:
                connection.rollback()
                raise HTTPException(status_code=404, detail = "Document not found")
        connection.commit()
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        print(f"deleting failed : {e} ")
        raise HTTPException(status_code=500, detail="Deleting document failed")

    ### Deleting the file form the s3 as well 
    s3.delete_object(Bucket = BUCKET_NAME, Key = f"uploads/{file_id}/{file_name}")
    return {"deleted": file_id}

    

