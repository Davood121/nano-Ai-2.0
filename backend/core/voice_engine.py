import asyncio
import edge_tts
import os
import re
import random
from pathlib import Path

class VoiceEngine:
    def __init__(self):
        # Use a natural-sounding voice
        self.voice = "en-US-AriaNeural"  # Female, natural
        # Alternative: "en-US-GuyNeural" for male voice
        self.audio_dir = Path("audio_cache")
        self.audio_dir.mkdir(exist_ok=True)
        
    def clean_text(self, text: str) -> str:
        """Remove markdown and clean text for speech."""
        clean = text
        # Remove markdown headers
        clean = re.sub(r'^#{1,6}\s+', '', clean, flags=re.MULTILINE)
        # Remove bold/italic
        clean = re.sub(r'\*\*(.+?)\*\*', r'\1', clean)
        clean = re.sub(r'\*(.+?)\*', r'\1', clean)
        clean = re.sub(r'__(.+?)__', r'\1', clean)
        clean = re.sub(r'_(.+?)_', r'\1', clean)
        # Remove code blocks
        clean = re.sub(r'```[\s\S]*?```', '', clean)
        clean = re.sub(r'`(.+?)`', r'\1', clean)
        # Remove links but keep text
        clean = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', clean)
        # Remove list markers
        clean = re.sub(r'^\s*[-*+]\s+', '', clean, flags=re.MULTILINE)
        clean = re.sub(r'^\s*\d+\.\s+', '', clean, flags=re.MULTILINE)
        # Clean whitespace
        clean = re.sub(r'\n{3,}', '\n\n', clean)
        return clean.strip()
    
    def add_human_like_patterns(self, text: str, emotion_state: dict) -> str:
        """Add natural speech patterns like breathing, pauses, and filler words."""
        sentences = re.split(r'([.!?]+)', text)
        enhanced = []
        
        # Emotion-based filler words and patterns
        stress_level = emotion_state.get('stress', 0)
        calm_level = emotion_state.get('calm', 0)
        curiosity_level = emotion_state.get('curiosity', 0)
        
        for i, part in enumerate(sentences):
            if not part.strip():
                continue
                
            # Add breathing sounds at sentence boundaries
            if i > 0 and random.random() < 0.3:
                enhanced.append("... ")  # Natural pause (edge-tts interprets as breath)
            
            # Add filler words based on emotion
            if stress_level > 0.6 and random.random() < 0.4:
                # When stressed, add hesitation
                fillers = ["umm", "uh", "well"]
                enhanced.append(random.choice(fillers) + "... ")
            elif curiosity_level > 0.6 and random.random() < 0.3:
                # When curious, add thoughtful pauses
                fillers = ["hmm", "let me think", "ah"]
                enhanced.append(random.choice(fillers) + "... ")
            elif calm_level > 0.6 and random.random() < 0.2:
                # When calm, add gentle pauses
                enhanced.append("... ")
            
            enhanced.append(part)
        
        result = ''.join(enhanced)
        
        # Add natural breathing at longer pauses
        result = re.sub(r'\.\s+', lambda m: '. ... ' if random.random() < 0.25 else '. ', result)
        
        return result
    
    async def generate_speech(self, text: str, emotion_state: dict, output_file: str):
        """Generate speech audio file using edge-tts with human-like patterns."""
        try:
            clean_text = self.clean_text(text)
            if not clean_text:
                return None
            
            # Add human-like speech patterns
            enhanced_text = self.add_human_like_patterns(clean_text, emotion_state)
                
            # Emotion-adaptive voice parameters
            rate = "+0%"
            pitch = "+0Hz"
            volume = "+0%"
            
            if emotion_state.get('stress', 0) > 0.6:
                rate = "+15%"
                pitch = "+5Hz"
                volume = "+10%"  # Slightly louder when stressed
            elif emotion_state.get('calm', 0) > 0.6:
                rate = "-8%"
                pitch = "-3Hz"
                volume = "-5%"  # Softer when calm
            elif emotion_state.get('joy', 0) > 0.6:
                rate = "+10%"
                pitch = "+8Hz"
                volume = "+5%"
            elif emotion_state.get('focus', 0) > 0.6:
                rate = "-5%"
                pitch = "+0Hz"
            
            communicate = edge_tts.Communicate(
                enhanced_text, 
                self.voice, 
                rate=rate, 
                pitch=pitch,
                volume=volume
            )
            
            # Generate audio with timeout
            await asyncio.wait_for(communicate.save(output_file), timeout=30.0)
            return output_file
            
        except asyncio.TimeoutError:
            print(f"Voice generation timeout for: {text[:50]}...")
            return None
        except Exception as e:
            print(f"Voice generation error: {e}")
            return None
