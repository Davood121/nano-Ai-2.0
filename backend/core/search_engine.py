from duckduckgo_search import DDGS
import re
import logging
from typing import List, Dict, Optional

logger = logging.getLogger("NanoAI_Search")

class SearchEngine:
    def __init__(self):
        self.ddgs = DDGS()
        
        # Keywords that trigger search
        self.search_triggers = [
            'latest', 'current', 'recent', 'today', 'news', 'breaking',
            'weather', 'stock', 'price', 'update', '2024', '2025', '2026',
            'happening', 'now', 'this week', 'this month', 'trending'
        ]
        
        # Keywords that trigger image search
        self.image_triggers = [
            'show me', 'picture', 'photo', 'image', 'images', 'photos',
            'look like', 'looks like', 'what does', 'how does', 'visual',
            'see', 'view', 'display'
        ]
    
    def should_search(self, query: str) -> bool:
        """Determine if query needs web search."""
        query_lower = query.lower()
        
        # Check for trigger keywords
        for trigger in self.search_triggers:
            if trigger in query_lower:
                return True
        
        # Check for question words that often need current info
        question_patterns = [
            r'\bwhat(?:\'s| is)\b.*\b(happening|new|latest)',
            r'\bhow much\b.*\b(cost|price)',
            r'\bwhen (?:is|was|will)\b',
            r'\bwhere (?:is|can)\b'
        ]
        
        for pattern in question_patterns:
            if re.search(pattern, query_lower):
                return True
        
        return False
    
    def should_search_images(self, query: str) -> bool:
        """Determine if query needs image search."""
        query_lower = query.lower()
        
        for trigger in self.image_triggers:
            if trigger in query_lower:
                return True
        
        return False
    
    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """Perform web search and return results."""
        try:
            logger.info(f"Searching for: {query}")
            
            # Perform search
            results = []
            search_results = self.ddgs.text(query, max_results=max_results)
            
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'snippet': result.get('body', ''),
                    'url': result.get('href', ''),
                    'source': self._extract_domain(result.get('href', ''))
                })
            
            logger.info(f"Found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return []
    
    def search_images(self, query: str, max_results: int = 6) -> List[Dict]:
        """Perform image search and return image URLs."""
        try:
            logger.info(f"Searching images for: {query}")
            
            images = []
            image_results = self.ddgs.images(query, max_results=max_results)
            
            for result in image_results:
                images.append({
                    'url': result.get('image', ''),
                    'thumbnail': result.get('thumbnail', ''),
                    'title': result.get('title', ''),
                    'source': result.get('source', '')
                })
            
            logger.info(f"Found {len(images)} images")
            return images
            
        except Exception as e:
            logger.error(f"Image search error: {e}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            match = re.search(r'https?://(?:www\.)?([^/]+)', url)
            if match:
                return match.group(1)
            return url
        except:
            return url
    
    def format_results(self, results: List[Dict]) -> str:
        """Format search results for LLM context."""
        if not results:
            return "No search results found."
        
        formatted = "Web Search Results:\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. **{result['title']}**\n"
            formatted += f"   {result['snippet']}\n"
            formatted += f"   Source: {result['source']}\n\n"
        
        return formatted
    
    def get_citations(self, results: List[Dict]) -> List[str]:
        """Extract URLs for citations."""
        return [r['url'] for r in results if r.get('url')]
