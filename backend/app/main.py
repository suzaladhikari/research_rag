from fastapi import FastAPI 
import requests

app = FastAPI(title='SentinelRAG')
@app.get("/")
def health_check():
    return {"status": "ok"}

