from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import logging
import asyncio
import os
import subprocess
from pathlib import Path
from core.emotion_engine import EmotionEngine
from core.planner import CognitivePlanner
from core.voice_engine import VoiceEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NanoAI")

app = FastAPI(title="NanoAI 2.0")

# CORS (Allow all for local development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Modules
emotion_engine = EmotionEngine()
planner = CognitivePlanner()
voice_engine = VoiceEngine()

# Mount audio directory for serving audio files
app.mount("/audio", StaticFiles(directory="audio_cache"), name="audio")

@app.get("/")
async def root():
    return {"status": "online", "system": "NanoAI 2.0", "mood": emotion_engine.get_current_state()}

# Settings Model
class SettingsUpdate(BaseModel):
    model_name: str = None
    context_window: int = None
    max_tokens: int = None
    temperature: float = None
    top_p: float = None

@app.get("/api/models")
async def get_available_models():
    """Get list of available Ollama models."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if parts:
                        model_name = parts[0]
                        models.append({"name": model_name, "size": parts[1] if len(parts) > 1 else "unknown"})
            return {"models": models}
        else:
            return {"models": [], "error": "Failed to fetch models"}
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return {"models": [], "error": str(e)}

@app.get("/api/settings")
async def get_settings():
    """Get current LLM settings."""
    return planner.get_settings()

@app.post("/api/settings")
async def update_settings(settings: SettingsUpdate):
    """Update LLM settings."""
    success = planner.update_settings(
        model_name=settings.model_name,
        context_window=settings.context_window,
        max_tokens=settings.max_tokens,
        temperature=settings.temperature,
        top_p=settings.top_p
    )
    
    if success:
        return {"status": "success", "settings": planner.get_settings()}
    else:
        return {"status": "error", "message": "Failed to update settings"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("Client connected")
    
    try:
        while True:
            # Receive text from client
            data = await websocket.receive_text()
            logger.info(f"Received: {data}")
            
            # 1. Perception & Emotion Analysis
            current_emotion = emotion_engine.update_state(data)
            
            # 2. Cognitive Planning & Response Generation
            ai_response = planner.process_input(data, current_emotion)
            
            # 3. Generate audio file
            audio_filename = f"response_{id(data)}.mp3"
            audio_path = voice_engine.audio_dir / audio_filename
            
            try:
                await voice_engine.generate_speech(
                    ai_response["text"], 
                    current_emotion, 
                    str(audio_path)
                )
                audio_url = f"/audio/{audio_filename}"
            except Exception as e:
                logger.error(f"Voice generation error: {e}")
                audio_url = None
            
            # 4. Send back structured response
            response_payload = {
                "text": ai_response["text"],
                "emotion_state": current_emotion,
                "thinking": False,
                "conversational_mode": ai_response.get("mode", "neutral"),
                "audio_url": audio_url,
                "search_performed": ai_response.get("search_performed", False),
                "sources": ai_response.get("sources", []),
                "images": ai_response.get("images", [])
            }
            
            await websocket.send_text(json.dumps(response_payload))
            
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"Error: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
