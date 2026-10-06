import boto3
import json 
import urllib.parse
from dotenv import load_dotenv
import os 
import psycopg2
from pgvector.psycopg2 import register_vector
import tempfile
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


### Creating connection with the database 
database = psycopg2.connect(os.getenv("DATABASE_URL")) ## Connecting with the database
connection = register_vector(database) ##The connection now accepts the column with the vecor format as well

### Tranformer model 
sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
load_dotenv()
SQS_URL = os.getenv("SQS_URL")
sqs = boto3.client("sqs", region_name="us-east-1")
s3 = boto3.client("s3", region_name="us-east-1")


### Extracting the text from the pdf 
def extract_text(path: str) -> str:
    reader = PdfReader(path)
    pages = [page.extract_text() or "" for page in reader.pages] ## Extracted the text of each page
    return "\n".join(pages).strip()

### Editing the chunks 
def chunk_text(text, chunk_size: int = 1000, overlap: int = 100) -> list[str]: ## Each chunk will be the size of 1000
    chunks = []
    start = 0 
    while start < len(text):
        chunks.append(text[start:start+chunk_size])
        start += chunk_size - overlap
    return chunks
## Creating the embedding vectors for the chunks 
def vectorize_chunks(chunks: list[str]) ->list[list[float]]: ## Each vector will be the size of 384 
    vectors = sentence_model.encode(
        chunks, 
        batch_size=64, 
        normalize_embeddings=True,
        show_progress_bar=False
    ) 
    return vectors.tolist()

def process_file(bucket_name:str, key:str) -> None:
    ## Creating a temp directory just to store the file, the directory will be deleted once the whole with command gets deleted
    with tempfile.TemporaryDirectory() as tmp_dir:
        local_path = os.path.join(tmp_dir, os.path.basename(key))
        s3.download_file(bucket_name, key, local_path)
        size = os.path.getsize(local_path)
        file_id = key.split("/")[1]
        print(f"Download s3://{bucket_name}/{key}, (size = {size})")
        text = extract_text(local_path)
        if not text:
            print(f"no text found in {key}")
        chunks = chunk_text(text)
        vectors = vectorize_chunks(chunks)

        print(f"For the text with size {len(text)} total of {len(chunks[0])} chunks have been created")
        print(f"For the text with size {len(text)} total of {len(vectors[0])} vectors have been created")
while True: 
    respones = sqs.receive_message(
        QueueUrl = SQS_URL,  ## Extracting the message from the given queue
        MaxNumberOfMessages = 5,  ## Maximum number of message to pollout at once
        WaitTimeSeconds = 20 ## Total Wait time 
    )
    for msg in respones.get("Messages", []):
        body = json.loads(msg["Body"])
    ### Skipping the one time test message that s3 sends 
        if body.get("Event") == 's3:TestEvent':
            sqs.delete_message(QueueUrl = SQS_URL, ReceiptHandle = msg["ReceiptHandle"] )
            continue

        ### Looping through the sqs messages

        for record in body["Records"]:
            bucket_name = record['s3']['bucket']['name']## Extracting the name of the bucket
            uploaded_file = record['s3']['object']['key'] ## Name of the file
            key = urllib.parse.unquote_plus(uploaded_file) ## This will give the format of  filename the way it is stored in the s3 
            process_file(bucket_name, key)

        sqs.delete_message(QueueUrl=SQS_URL, ReceiptHandle=msg["ReceiptHandle"])