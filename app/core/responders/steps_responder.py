from core.llm_client import get_llm_client
from core.prompts import load_prompt
from core.logging import setup_logger

logger = setup_logger(__name__)

def generate_steps(prompt: str) -> str:
    """Generate step-by-step explanation"""
    client = get_llm_client()
    full_prompt = load_prompt("prompt_steps").format(message=prompt)
    logger.debug(f"Steps prompt length: {len(full_prompt)}")
    return client.generate(full_prompt, stream=False)