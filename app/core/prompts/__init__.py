from pathlib import Path

PROMPT_DIR = Path(__file__).parent

def load_prompt(name: str) -> str:
    path = PROMPT_DIR / f"{name}.txt"
    if not path.exists():
        raise FileNotFoundError(f"Prompt {name}.txt not found")
    return path.read_text()