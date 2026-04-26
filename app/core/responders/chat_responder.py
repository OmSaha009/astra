from core.llm_client import get_llm_client
from core.prompts import load_prompt
from core.logging import setup_logger

logger = setup_logger(__name__)

def generate_chat_response(message: str, context: str) -> str:
    """Generate chat response"""
    client = get_llm_client()
    prompt = load_prompt("prompt_chat").format(message=message, context=context)
    logger.debug(f"Chat prompt length: {len(prompt)}")
    return client.generate(prompt, stream=True)