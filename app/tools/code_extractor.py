import re

def extract_code(text: str) -> tuple[str, str | None]:

    print("=================RAW TEXT TO MATCH FOR CODE=============")
    print(repr(text))
    print("========================================================")
    pattern = r'```python\s*(.*?)```'
    match = re.match(pattern, text, re.DOTALL)

    print(match if match else "NO CODE MATCHED")

    if match:
        code = match.group(1).strip()

        text_without_code = re.sub(pattern, "[CODE BLOCK REMOVED]", text, flags=re.DOTALL)
        return text_without_code, code

    pattern2 = r'```\s*(.*?)```'
    match2 = re.search(pattern2, text, re.DOTALL)
    
    if match2:
        print("USING MATCH 2")
        code = match2.group(1).strip()

        if code.startswith("python"):
            code = code[6:].strip()
        else:
            code = code

        text_without_code = re.sub(pattern2, '[CODE BLOCK REMOVED]', text, flags=re.DOTALL)
        return text_without_code, code

    return text, None