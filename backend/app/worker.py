import boto3
import json 
import urllib.parse
from dotenv import load_dotenv
import os 

load_dotenv()
SQS_URL = os.getenv("SQS_URL")
sqs = boto3.client("sqs", region_name="us-east-1")