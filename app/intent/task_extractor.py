import re

def regex_extract(message: str):
    msg = message.lower()

    patterns = [
        ("explain", r"(explain|what is|define)\s+(.*)"),
        ("solve", r"(solve|find|calculate)\s+(.*)"),
        ("derive", r"(derive|prove)\s+(.*)"),
        ("summarize", r"(summarize|summary of)\s+(.*)")
    ]

    for task, pattern in patterns:
        match = re.search(pattern, msg)
        if match:
            return {
                "task": task,
                "topic": match.group(2).strip(),
                "source": "regex"
            }

    return None

import spacy

nlp = spacy.load("en_core_web_sm")

TASK_VERBS = ["explain", "solve", "derive", "summarize", "define"]

def spacy_extract(message):
    doc = nlp(message.lower())

    for token in doc:
        if token.lemma_ == "derive":
            
            # look for object of derive
            topic_tokens = []

            for child in token.children:
                if child.dep_ in ["dobj", "pobj", "attr"]:
                    topic_tokens.extend([t.text for t in child.subtree])

            topic = " ".join(topic_tokens)

            return {
                "task": "derive",
                "topic": topic,
                "source": "spacy"
            }

import re

def score_result(result):
    score = 0

    topic = result.get("topic", "").strip()

    # 1. Length check (not too short, not too long)
    if 5 < len(topic) < 120:
        score += 2

    # 2. Avoid garbage phrases
    bad_words = ["how to", "tell me", "please", "can you"]
    if not any(word in topic for word in bad_words):
        score += 2

    # 3. Contains meaningful words (nouns-ish heuristic)
    if len(topic.split()) >= 3:
        score += 2

    # 4. Penalize full sentence reuse
    if topic.lower() != result.get("original", "").lower():
        score += 2

    return score

def extract_best(message):
    
    regex_result = regex_extract(message)
    spacy_result = spacy_extract(message)

    results = []

    if regex_result:
        results.append(regex_result)

    if spacy_result:
        results.append(spacy_result)
    
    if not results:
        return {
            "task": "conversation",
            "topic": message,
            "source": "default"
        }

    scored = [(res, score_result(res)) for res in results]

    # pick best
    best = max(scored, key=lambda x: x[1])[0]

    return best