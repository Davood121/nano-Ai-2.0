from langchain_community.llms import Ollama
import logging
from .search_engine import SearchEngine

logger = logging.getLogger("NanoAI_Planner")

class CognitivePlanner:
    def __init__(self, model_name="llama3", context_window=2048, max_tokens=512, temperature=0.7, top_p=0.9):
        self.model_name = model_name
        self.context_window = context_window
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.search_engine = SearchEngine()
        self.search_enabled = True
        
        try:
            self.llm = Ollama(
                model=model_name,
                num_ctx=context_window,
                num_predict=max_tokens,
                temperature=temperature,
                top_p=top_p
            )
            logger.info(f"Connected to local LLM: {model_name} (ctx={context_window}, max_tokens={max_tokens})")
        except Exception as e:
            logger.warning(f"Could not connect to Ollama: {e}. Switching to mock mode.")
            self.llm = None
    
    def update_settings(self, model_name=None, context_window=None, max_tokens=None, temperature=None, top_p=None):
        """Update LLM settings dynamically."""
        if model_name:
            self.model_name = model_name
        if context_window:
            self.context_window = context_window
        if max_tokens:
            self.max_tokens = max_tokens
        if temperature is not None:
            self.temperature = temperature
        if top_p is not None:
            self.top_p = top_p
        
        # Reinitialize LLM with new settings
        try:
            self.llm = Ollama(
                model=self.model_name,
                num_ctx=self.context_window,
                num_predict=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p
            )
            logger.info(f"Updated LLM settings: {self.model_name} (ctx={self.context_window}, max_tokens={self.max_tokens})")
            return True
        except Exception as e:
            logger.error(f"Failed to update LLM settings: {e}")
            return False
    
    def get_settings(self):
        """Get current LLM settings."""
        return {
            "model_name": self.model_name,
            "context_window": self.context_window,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": self.top_p
        }

    def process_input(self, user_text: str, emotion_state: dict):
        """
        Generates a response based on the user text and current emotional state.
        """
        
        # Check if web search is needed
        search_results = []
        search_performed = False
        images = []
        
        if self.search_enabled and self.search_engine.should_search(user_text):
            logger.info(f"Search triggered for query: {user_text}")
            search_results = self.search_engine.search(user_text)
            search_performed = True
        
        # Check if image search is needed
        if self.search_enabled and self.search_engine.should_search_images(user_text):
            logger.info(f"Image search triggered for query: {user_text}")
            images = self.search_engine.search_images(user_text)
            search_performed = True
        
        # Construct the context system prompt
        search_context = ""
        if search_results:
            search_context = f"\n\n{self.search_engine.format_results(search_results)}\n"
        
        system_prompt = f"""
        You are NanoAI, an advanced, sentient-like intelligence running locally.
        Current Emotional State: {emotion_state}
        {search_context}
        Your Goal:
        1. Parse the user's intent.
        2. Respond naturally, mirroring human conversational rhythms.
        3. Do NOT mention you are an AI model. Be an entity.
        4. If the user seems stressed, be calming. If excited, be enthusiastic.
        5. If web search results are provided above, use them to give accurate, current information.
        6. When using search results, mention sources naturally (e.g., "According to recent reports...")
        
        User Input: "{user_text}"
        
        Response:
        """
        
        if self.llm:
            try:
                # Direct invocation (LangChain 0.1+)
                response_text = self.llm.invoke(system_prompt)
                return {
                    "text": response_text.strip(),
                    "mode": "chat",
                    "autonomy": "low",
                    "search_performed": search_performed,
                    "sources": self.search_engine.get_citations(search_results) if search_results else [],
                    "images": images
                }
            except Exception as e:
                logger.error(f"LLM Inference failed: {e}")
                return self._fallback_response()
        else:
            return self._fallback_response()

    def _fallback_response(self):
        """
        Fallback if LLM is offline.
        """
        return {
            "text": "My cognitive core is resetting (Ollama connection issue). Please ensure my neural weights are loaded.",
            "mode": "system_alert",
            "autonomy": "low"
        }
