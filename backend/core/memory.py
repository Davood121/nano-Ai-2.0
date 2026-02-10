import json
import os

class MemorySystem:
    def __init__(self):
        self.short_term = []
        self.long_term_path = "memory.json"
        
        # Load existing memory
        if os.path.exists(self.long_term_path):
            with open(self.long_term_path, "r") as f:
                self.long_term = json.load(f)
        else:
            self.long_term = []

    def add_interaction(self, user_text, ai_response, emotion_state):
        entry = {
            "user": user_text,
            "ai": ai_response,
            "emotion": emotion_state
        }
        self.short_term.append(entry)
        self.long_term.append(entry)
        
        # Simple persistence (TODO: Replace with Vector DB)
        with open(self.long_term_path, "w") as f:
            json.dump(self.long_term, f, indent=4)

    def get_context(self, limit=5):
        return self.short_term[-limit:]
