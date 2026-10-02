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
        WaitTimeSeconds = 20 ## Total Wait time 
    )