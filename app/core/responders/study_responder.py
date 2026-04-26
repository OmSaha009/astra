from core.llm_client import get_llm_client
from core.prompts import load_prompt
from core.logging import setup_logger

logger = setup_logger(__name__)

def generate_study_response(message: str, context: str, topic: str) -> str:
    """Generate study/explanation response"""
    client = get_llm_client()
    prompt = load_prompt("prompt_study").format(
        message=message,
        context=context,
        topic=topic
    )
    logger.debug(f"Study prompt length: {len(prompt)}")
    return client.generate(prompt, stream=True)