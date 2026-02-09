from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict
import logging
from contextlib import asynccontextmanager

from .scraper import scrape_website
from .rag_engine import rag_engine
from .scheduler import start_scheduler, update_knowledge_base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start scheduler and perform initial scrape if empty
    start_scheduler()
    # Optional: Trigger an initial scrape on startup if DB is empty
    # For now, we leave it manual or scheduled
    yield
    # Shutdown logic if needed

app = FastAPI(title="OrbitThink Chatbot API", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for widget usage
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

@app.get("/")
def read_root():
    return {"status": "online", "service": "OrbitThink Chatbot Backend"}

@app.post("/api/scrape")
def trigger_scrape():
    """
    Manual endpoint to trigger scraping and updating the knowledge base.
    """
    try:
        data = scrape_website()
        if not data:
            raise HTTPException(status_code=500, detail="Scraping returned no data")
        
        success = rag_engine.add_documents(data)
        if not success:
             raise HTTPException(status_code=500, detail="Failed to update Vector DB")
             
        return {"status": "success", "message": "Knowledge base updated successfully"}
    except Exception as e:
        logger.error(f"Scrape failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint for the widget.
    """
    try:
        response_text = rag_engine.generate_response(request.message)
        return {"response": response_text}
    except Exception as e:
        logger.error(f"Chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
