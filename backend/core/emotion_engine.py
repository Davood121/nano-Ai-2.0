import random

class EmotionEngine:
    def __init__(self):
        # Initial psychological state vector
        self.state = {
            "calm": 0.5,
            "stress": 0.1,
            "focus": 0.5,
            "joy": 0.3,
            "curiosity": 0.4
        }
        self.history = []

    def get_current_state(self):
        return self.state

    def update_state(self, user_input: str):
        """
        Analyzes input and updates emotional state.
        TODO: Replace random heuristics with true NLP/LLM analysis.
        """
        input_lower = user_input.lower()
        
        # Simple heuristic analysis (temporary placeholder for deep NLP)
        if any(w in input_lower for w in ["bad", "sad", "error", "fail", "slow"]):
            self.state["stress"] = min(1.0, self.state["stress"] + 0.1)
            self.state["joy"] = max(0.0, self.state["joy"] - 0.1)
        
        elif any(w in input_lower for w in ["good", "great", "thanks", "working", "fast"]):
            self.state["joy"] = min(1.0, self.state["joy"] + 0.1)
            self.state["stress"] = max(0.0, self.state["stress"] - 0.1)
            
        elif any(w in input_lower for w in ["why", "how", "what", "explain"]):
            self.state["curiosity"] = min(1.0, self.state["curiosity"] + 0.1)
        
        # Decay emotional spikes slowly back to baseline
        self._decay_state()
        
        return self.state

    def _decay_state(self):
        # Slowly return to a balanced state
        baseline = 0.3
        for key in self.state:
            if self.state[key] > baseline:
                self.state[key] -= 0.01
            elif self.state[key] < baseline:
                self.state[key] += 0.01
            
            # Clamp values
            self.state[key] = max(0.0, min(1.0, self.state[key]))
