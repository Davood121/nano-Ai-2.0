# NanoAI 2.0 - Emotion-Aware AI System

A fully local, zero-cost, self-evolving, emotion-aware AI system with a futuristic glassmorphism interface.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.ai/) installed and running
- A local LLM model (e.g., `llama3`)

### Installation

1. **Install Python dependencies:**
```powershell
pip install -r requirements.txt
```

2. **Ensure Ollama is running with a model:**
```powershell
ollama serve
# In another terminal:
ollama pull llama3
```

### Running the System

1. **Start the Backend (AI Brain):**
```powershell
cd backend
python main.py
```
The server will start on `http://localhost:8000`

2. **Open the Frontend (UI):**
- Simply open `frontend/index.html` in your web browser
- Or run: `start frontend\index.html`

## 🧠 Architecture

### Backend (`backend/`)
- **`main.py`**: FastAPI WebSocket server
- **`core/emotion_engine.py`**: Emotion detection and psychological state tracking
- **`core/planner.py`**: LLM-powered cognitive planning and response generation
- **`core/memory.py`**: Conversation history and context management

### Frontend (`frontend/`)
- **`index.html`**: Glassmorphism UI structure
- **`style.css`**: Dark futuristic theme with neon accents
- **`script.js`**: WebSocket client with GSAP animations

## ✨ Features

- 🎭 **Emotion Detection**: Analyzes user sentiment and adapts responses
- 🧠 **Local LLM**: Powered by Ollama (fully offline)
- 🎨 **Futuristic UI**: Glassmorphism design with smooth animations
- 💬 **Real-time Chat**: WebSocket-based instant communication
- 🔒 **Privacy First**: Everything runs locally on your machine
- 💰 **Zero Cost**: No paid APIs or cloud services

## 🎨 UI Features

- Emotion-reactive color system
- Smooth GSAP animations
- Breathing "thinking" indicator
- Adaptive mood display
- Glassmorphism panels with backdrop blur

## 🔧 Configuration

Edit `backend/core/planner.py` to change the LLM model:
```python
self.llm = OllamaLLM(model="llama3")  # Change to your preferred model
```

## 📝 License

Open source - feel free to modify and extend!
