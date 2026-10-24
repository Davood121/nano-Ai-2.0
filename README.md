# NanoAI 2.0 - Emotion-Aware AI System

> **Project status:** Experimental prototype. Feature completeness and test coverage vary; see the setup instructions and verify behavior in your environment.

> Nano AI 2.0 - Compact artificial intelligence system with Python backend and web interface.

A fully local, zero-cost, self-evolving, emotion-aware AI system with a futuristic glassmorphism interface.

## Features

- **Emotion Detection** — Analyzes user sentiment in real-time and adapts responses accordingly
- **Local LLM** — Powered by Ollama, runs entirely offline with no API costs
- **Futuristic UI** — Glassmorphism design with neon accents and smooth GSAP animations
- **Real-Time Chat** — WebSocket-based instant communication with the AI brain
- **Privacy First** — Everything runs locally on your machine — zero data leaves your system
- **Zero Cost** — No paid APIs or cloud services required

## Quick Start

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.ai/) installed and running
- A local LLM model (e.g., `llama3`)

### Installation

```bash
# Install Python dependencies
pip install -r requirements.txt

# Ensure Ollama is running with a model
ollama pull llama3
```

### Running the System

**Start the Backend (AI Brain):**
```bash
cd backend
python main.py
```
Server starts on `http://localhost:8000`

**Open the Frontend (UI):**
- Open `frontend/index.html` in your browser

## Architecture

### Backend (`backend/`)
| Module | Purpose |
|--------|---------|
| `main.py` | FastAPI WebSocket server |
| `core/emotion_engine.py` | Emotion detection and psychological state tracking |
| `core/planner.py` | LLM-powered cognitive planning and response generation |
| `core/memory.py` | Conversation history and context management |

### Frontend (`frontend/`)
| File | Purpose |
|------|---------|
| `index.html` | Glassmorphism UI structure |
| `style.css` | Dark futuristic theme with neon accents |
| `script.js` | WebSocket client with GSAP animations |

## UI Features

- Emotion-reactive color system that changes with user sentiment
- Smooth GSAP animations for polished interactions
- Breathing "thinking" indicator during AI processing
- Adaptive mood display panel
- Glassmorphism panels with backdrop blur effects

## Configuration

Edit `backend/core/planner.py` to change the LLM model:
```python
self.llm = OllamaLLM(model="llama3")  # Change to your preferred model
```

## Tech Stack

- **Backend:** Python, FastAPI, Ollama
- **Frontend:** HTML5, CSS3, JavaScript, GSAP
- **Communication:** WebSockets

## License

Open source — feel free to modify and extend.

## Links

- [GitHub Repository](https://github.com/Davood121/nano-Ai-2.0)