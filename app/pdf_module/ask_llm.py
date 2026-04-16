import requests

def ask_llm():
    prompt = f'''
    WHAT IS BERNOULLI's PRINCIPLE and give a proper example.
'''
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]