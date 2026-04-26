# routes/task_extractor.py
import re
import spacy
from core.logging import setup_logger

logger = setup_logger(__name__)

# ============================================================
# Constants
# ============================================================

MIN_TOPIC_LENGTH = 5
MAX_TOPIC_LENGTH = 120
MIN_WORD_COUNT = 3
BAD_PHRASES = ["how to", "tell me", "please", "can you"]

TASK_PATTERNS = [
    ("explain", r"(explain|what is|define)\s+(.*)"),
    ("solve", r"(solve|find|calculate)\s+(.*)"),
    ("derive", r"(derive|prove)\s+(.*)"),
    ("summarize", r"(summarize|summary of)\s+(.*)"),
]

TASK_VERBS = ["explain", "solve", "derive", "summarize", "define"]

# Load spaCy model (lazy loading)
_nlp = None

def get_nlp():
    global _nlp
    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
            logger.info("SpaCy model loaded")
        except OSError:
            logger.error("SpaCy model not found. Run: python -m spacy download en_core_web_sm")
            raise
    return _nlp


# ============================================================
# Extractors
# ============================================================

def regex_extract(message: str) -> dict | None:
    """Extract task using regex patterns"""
    msg = message.lower()
    
    for task, pattern in TASK_PATTERNS:
        match = re.search(pattern, msg)
        if match:
            logger.debug(f"Regex extracted: {task} - {match.group(2)[:50]}...")
            return {
                "task": task,
                "topic": match.group(2).strip(),
                "source": "regex"
            }
    return None


def spacy_extract(message: str) -> dict | None:
    """Extract task using spaCy dependency parsing"""
    nlp = get_nlp()
    doc = nlp(message.lower())
    
    for token in doc:
        if token.lemma_ in TASK_VERBS:
            # Look for object of the verb
            topic_tokens = []
            for child in token.children:
                if child.dep_ in ["dobj", "pobj", "attr"]:
                    topic_tokens.extend([t.text for t in child.subtree])
            
            if topic_tokens:
                topic = " ".join(topic_tokens)
                logger.debug(f"SpaCy extracted: {token.lemma_} - {topic[:50]}...")
                return {
                    "task": token.lemma_,
                    "topic": topic,
                    "source": "spacy"
                }
    return None


# ============================================================
# Scoring
# ============================================================

def score_result(result: dict) -> int:
    """Score extraction quality (higher is better)"""
    topic = result.get("topic", "").strip()
    score = 0
    
    # Length check
    if MIN_TOPIC_LENGTH < len(topic) < MAX_TOPIC_LENGTH:
        score += 2
    
    # Avoid garbage phrases
    if not any(bad in topic.lower() for bad in BAD_PHRASES):
        score += 2
    
    # Contains meaningful words
    if len(topic.split()) >= MIN_WORD_COUNT:
        score += 2
    
    # Penalize full sentence reuse
    original = result.get("original", "")
    if original and topic.lower() != original.lower():
        score += 2
    
    return score


# ============================================================
# Main function
# ============================================================

def extract_best(message: str) -> dict:
    """
    Extract best task and topic from message.
    Returns: {"task": str, "topic": str, "source": str}
    """
    logger.debug(f"Extracting task from: {message[:50]}...")
    
    regex_result = regex_extract(message)
    spacy_result = spacy_extract(message)
    
    results = []
    if regex_result:
        results.append(regex_result)
    if spacy_result:
        results.append(spacy_result)
    
    # Default if nothing found
    if not results:
        logger.info("No task extracted, defaulting to conversation")
        return {
            "task": "conversation",
            "topic": message,
            "source": "default"
        }
    
    # Score and pick best
    scored = [(res, score_result(res)) for res in results]
    best = max(scored, key=lambda x: x[1])[0]
    
    logger.debug(f"Best extraction: {best['task']} - {best['topic'][:50]}... (source: {best['source']})")
    return best