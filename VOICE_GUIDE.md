# Voice Output Feature Guide

## Overview
NanoAI 2.0 now includes **human-like voice output** that adapts to the AI's emotional state.

## How to Use

### Enabling Voice
1. Look for the **speaker icon** in the top-right corner of the interface
2. Click the speaker icon to toggle voice output
3. When enabled, the icon turns **cyan** and you'll hear "Voice output enabled"
4. The AI will now speak all responses aloud

### Disabling Voice
- Click the speaker icon again to disable
- Any ongoing speech will be cancelled immediately

## Emotion-Adaptive Voice

The AI's voice changes based on its emotional state:

| Emotion State | Voice Characteristics |
|--------------|----------------------|
| **Calm** | Slower rate (0.9x), slightly lower pitch (0.95) |
| **Stressed** | Faster rate (1.2x), higher pitch (1.1) |
| **Joyful** | Higher pitch (1.15), faster rate (1.1) |
| **Focused** | Measured rate (0.95), neutral pitch (1.0) |

## Visual Indicators

### Speaking Indicator
- Appears next to the voice toggle when AI is speaking
- Animated vertical bars that pulse in sync
- Automatically hides when speech completes

## Technical Details

- **Technology**: Web Speech API (built into modern browsers)
- **Zero Cost**: No external APIs or services required
- **Privacy**: All processing happens locally in your browser
- **Voice Selection**: Automatically selects the best natural-sounding English voice available

## Browser Compatibility

Works in:
- ✅ Chrome/Edge (recommended)
- ✅ Safari
- ✅ Firefox (limited voice options)

## Tips

1. **First Use**: The browser may ask for permission to use speech synthesis
2. **Voice Quality**: Chrome/Edge typically have the best natural voices
3. **Interruption**: Click the voice toggle to stop ongoing speech
4. **Emotion Testing**: Try different conversation tones to hear voice adaptation:
   - Say "I'm stressed" → Faster, higher voice
   - Say "I'm feeling calm" → Slower, softer voice
   - Say "This is great!" → Joyful, energetic voice
