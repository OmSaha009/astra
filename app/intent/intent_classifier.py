from core.ollama_call import intent_classification

command_keys = ["open", "browse", "play", "extract"]
study_keys = ["explain", "define", "show", "tell"]

LLM_THRESHOLD = 0.6

source = ""

def classify_intent(text):
    prompt = text.lower().strip()
    words = prompt.split()


    command_score = 0
    study_score = 0

    intent = "" 
    score = 0
    other = 0

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
        confidence = 0
    elif command_score > study_score:
        intent = "command"
        score = command_score
        other = study_score
    elif study_score > command_score:
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
        print("LLM CALLBACK")
        print("wait")
        response = str(intent_classification(prompt)).replace(" ", '')
        response = response.split(',')
        intent = response[0]
        confidence = response[1]
        source = "llm"

    response_obj = {
        "intent": intent,
        "confidence": confidence,
        "source": source
    }

    return response_obj
