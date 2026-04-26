from core.llm_client import get_llm_client
from core.prompts import load_prompt
from core.logging import setup_logger

logger = setup_logger(__name__)

def generate_math_response(message: str, context: str, task: str, topic: str) -> str:
    """Generate math solution code"""
    client = get_llm_client()
    prompt = load_prompt("prompt_math").format(
        message=message,
        context=context,
        task=task,
        topic=topic
    )
    logger.debug(f"Math prompt length: {len(prompt)}")
    return client.generate(prompt, stream=True)  # Return streaming response