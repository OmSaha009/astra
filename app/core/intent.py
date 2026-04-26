from core.llm_client import get_llm_client
from core.prompts import load_prompt
from core.logging import setup_logger

logger = setup_logger(__name__)

command_keys = ["open", "browse", "play", "extract"]
study_keys = ["explain", "define", "show", "tell"]
LLM_THRESHOLD = 0.6

def _llm_classification(text: str) -> tuple:
    """Call LLM for intent classification"""
    client = get_llm_client()
    prompt = load_prompt("prompt_intent").format(question=text)
    client = get_llm_client()

    response = client.generate(prompt=prompt)
    cleaned = response.replace(" ", "")
    parts = cleaned.split(',')
    
    if len(parts) >= 2:
        return parts[0], float(parts[1])
    return "chat", 0.5


def classify_intent(text: str) -> dict:
    prompt = text.lower().strip()
    words = prompt.split()
    score = 0
    other = 0
    command_score = 0
    study_score = 0

    for word in words:
        if word in command_keys:
            command_score += 2
        if word in study_keys:
            study_score += 2

    if words and words[0] in command_keys:
        command_score += 1
    if words and words[0] in study_keys:
        study_score += 1

    if command_score == 0 and study_score == 0:
        confidence = 0.5
        intent = "chat"
    elif command_score > study_score:
        intent = "command"
        score = command_score
        other = study_score
    else:
        intent = "study"
        score = study_score
        other = command_score

    if score >= 3 and other == 0:
        confidence = 1.0
    elif score > other:
        confidence = 0.7
    else:
        confidence = 0.5

    source = "rule"

    if confidence <= LLM_THRESHOLD:
        logger.info(f"LLM fallback for: {text[:50]}...")
        intent, confidence = _llm_classification(text)
        source = "llm"

    return {
        "intent": intent,
        "confidence": confidence,
        "source": source
    }