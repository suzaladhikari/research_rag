from fastapi import FastAPI 
from backend.app.routes.post import router as posting_router 

app = FastAPI(title = 'SentinelRAG')
app.include_router(posting_router)
