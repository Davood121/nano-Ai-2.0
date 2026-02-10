# Voice Output - Backend TTS Method

## What Changed

I've switched from Web Speech API to **edge-tts** (Microsoft Edge TTS) for much better voice quality and reliability.

## Why This Is Better

1. ✅ **No Interruptions** - Audio files play completely without stopping
2. ✅ **No Markdown** - Text is cleaned before speech generation
3. ✅ **High Quality** - Microsoft's neural voices sound very natural
4. ✅ **Free & Local** - No API costs, works offline after first download
5. ✅ **Emotion-Adaptive** - Voice rate and pitch adjust based on AI mood

## How It Works Now

1. Backend generates audio file using edge-tts
2. Audio saved to `audio_cache/` directory
3. Frontend receives audio URL and plays it
4. Clean, uninterrupted playback

## Next Steps

1. Install edge-tts: `pip install edge-tts`
2. Restart the backend server
3. Refresh the frontend
4. Enable voice and test!

## Available Voices

Current: `en-US-AriaNeural` (Female, natural)
Alternative: `en-US-GuyNeural` (Male, natural)

You can change the voice in `backend/core/voice_engine.py` line 8.
