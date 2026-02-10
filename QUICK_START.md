# NanoAI 2.0 - Quick Start Guide

## 🚀 One-Click Startup

### Windows
Simply **double-click** `START_NANOAI.bat` to launch everything!

This will automatically:
1. ✅ Start Ollama server (if not running)
2. ✅ Start Backend server (http://localhost:8000)
3. ✅ Open Frontend in your browser

### To Stop
Double-click `STOP_NANOAI.bat` to shut down all services.

---

## 📋 Manual Startup (Alternative)

If you prefer to start components individually:

### 1. Start Ollama
```bash
ollama serve
```

### 2. Start Backend
```bash
cd backend
python main.py
```

### 3. Open Frontend
Open `frontend/index.html` in your browser

---

## 🎯 Quick Test

After starting, try these queries:

**Regular Chat:**
- "Hello, how are you?"
- "Explain quantum physics"

**Web Search (Auto-triggers):**
- "What's the latest news about AI?"
- "Current weather today"
- "Recent updates on technology"

**Voice Output:**
- Click the 🔊 speaker icon in the sidebar
- Send a message and hear the AI speak!

**Settings:**
- Click ⚙️ in the header
- Switch Ollama models
- Adjust performance (Speed/Balanced/Quality presets)

---

## 🔧 Troubleshooting

**Backend won't start:**
- Make sure Python is installed
- Install dependencies: `pip install -r requirements.txt`

**Ollama not found:**
- Install Ollama from https://ollama.ai
- Pull a model: `ollama pull llama3`

**Voice not working:**
- Restart backend after installing `edge-tts`
- Check browser console for errors

**Search not working:**
- Install: `pip install duckduckgo-search`
- Restart backend

---

## 📁 Project Structure

```
nano Ai_2..0/
├── START_NANOAI.bat       ← Double-click to start!
├── STOP_NANOAI.bat        ← Double-click to stop
├── backend/
│   ├── main.py            ← FastAPI server
│   └── core/
│       ├── planner.py     ← LLM integration
│       ├── emotion_engine.py
│       ├── voice_engine.py
│       └── search_engine.py
├── frontend/
│   ├── index.html         ← Main UI
│   ├── script.js          ← Frontend logic
│   ├── settings.js        ← Settings panel
│   └── style.css          ← Styling
└── requirements.txt       ← Python dependencies
```

---

## 🎨 Features

- ✨ **Emotion-Aware AI** - Adapts tone based on your mood
- 🔊 **Voice Output** - Human-like speech with emotion
- 🔍 **Auto Web Search** - Fetches latest information
- ⚙️ **Model Switcher** - Change Ollama models on-the-fly
- 🎛️ **Performance Tuning** - Speed/Balanced/Quality presets
- 💾 **Local & Private** - Everything runs on your machine
- 🆓 **Zero Cost** - No API fees, completely free

---

## 💡 Tips

1. **For faster responses:** Use Speed preset in settings
2. **For better quality:** Use Quality preset
3. **Voice customization:** Edit `backend/core/voice_engine.py` line 11 to change voice
4. **Search toggle:** Disable in code if you don't want auto-search

Enjoy your AI! 🚀
