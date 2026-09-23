from fastapi import FastAPI 
from app.routes.events import router as events_router 

app = FastAPI(title = 'SentinelRAG')
app.include_router(events_router)

