import requests
from core.logging import setup_logger

logger = setup_logger(__name__)

API_URL = "http://localhost:11434/api/generate"

class LLMClient:
    def __init__(self, model="qwen2.5:7b"):
        self.model = model
        logger.info(f"LLMClient initialized with {model}")

    def generate(self, prompt: str, stream: bool = False):
        logger.debug(f"Generating: {len(prompt)} chars")
        try:
            response = requests.post(
                API_URL,
                json = {
                    "model": self.model,
                    "prompt": prompt,
                    "stream": stream
                },
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                return response
            
            return response.json().get("response", "")
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Ollama service not running")
            raise Exception("Ollama service not running")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            raise Exception(f"Ollama returned error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
    
_client = None

def get_llm_client():
    global _client
    if _client is None:
        _client = LLMClient()
    return _client