"""
FastAPI Server - HTTP API for the Personal Assistant Agent
"""

import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.agent import PersonalAssistantAgent
from utils.auth import authenticate_google

# Load .env from backend directory
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))

# Global agent instance
agent: PersonalAssistantAgent = None


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize agent on startup."""
    global agent
    
    print("[INFO] Starting Personal Assistant Server...")
    
    # Authenticate with Google
    google_creds = authenticate_google()
    if not google_creds:
        print("[ERROR] Failed to authenticate with Google")
        raise RuntimeError("Google authentication failed")
    
    print("[OK] Google authentication successful")
    
    # Get Gemini API key
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("[ERROR] GEMINI_API_KEY not found in .env")
        raise RuntimeError("GEMINI_API_KEY not configured")
    
    # Initialize agent
    agent = PersonalAssistantAgent(
        gemini_api_key=gemini_api_key,
        google_creds=google_creds
    )
    
    print("[OK] Agent initialized")
    print("[OK] Server ready at http://localhost:8000")
    
    yield
    
    print("[INFO] Shutting down...")


app = FastAPI(
    title="Personal Assistant API",
    description="AI-powered personal assistant with Gmail and Calendar integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "agent_ready": agent is not None}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message and return the agent's response.
    """
    if not agent:
        raise HTTPException(status_code=503, detail="Agent not initialized")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        response = agent.process_request(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/reset")
async def reset_conversation():
    """Reset the conversation history."""
    if agent:
        agent.reset_conversation()
    return {"status": "conversation reset"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
