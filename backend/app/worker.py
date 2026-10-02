import boto3
import json 
import urllib.parse
from dotenv import load_dotenv
import os 

load_dotenv()
SQS_URL = os.getenv("SQS_URL")
sqs = boto3.client("sqs", region_name="us-east-1")

while True: 
    respones = sqs.receive_message(
        QueueUrl = SQS_URL,  ## Extracting the message from the given queue
        MaxNumberOfMessages = 5,  ## Maximum number of message to pollout at once
        WaitTimeSeconds = 2 ## Total Wait time 
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
            print(f"New Upload: {bucket_name}/{key}")

        sqs.delete_message(QueueUrl=SQS_URL, ReceiptHandle=msg["ReceiptHandle"])