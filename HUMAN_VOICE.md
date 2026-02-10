# Human-Like Voice Enhancement

## What's New

Your AI now speaks with **natural human-like patterns**!

### Emotional Voice Features

**Breathing & Pauses:**
- Natural breathing sounds between sentences (represented as "...")
- Random pauses for more realistic speech flow

**Emotion-Based Filler Words:**

| Emotion | Filler Words | Behavior |
|---------|-------------|----------|
| **Stressed** | "umm", "uh", "well" | 40% chance of hesitation |
| **Curious** | "hmm", "let me think", "ah" | 30% chance of thoughtful pause |
| **Calm** | Gentle pauses | 20% chance of soft breath |

**Volume Adjustments:**
- **Stressed**: +10% louder (more urgent)
- **Calm**: -5% softer (more soothing)
- **Joyful**: +5% louder (more energetic)

### How It Works

1. Text is cleaned (markdown removed)
2. Human-like patterns are added based on emotion
3. Filler words inserted randomly at appropriate moments
4. Natural breathing pauses added between sentences
5. Voice parameters (pitch, rate, volume) adjusted for emotion

### Example

**Input:** "I can help you with that."

**Stressed Output:** "Umm... I can help you with that. ... Well, let me know if you need more."

**Calm Output:** "... I can help you with that. ... Just let me know."

**Curious Output:** "Hmm... I can help you with that. ... Ah, let me think about the best approach."

## To Test

1. Restart your backend server (Ctrl+C, then `python backend/main.py`)
2. Refresh the frontend
3. Enable voice and chat with different emotional tones
4. Listen for the natural breathing, pauses, and filler words!
