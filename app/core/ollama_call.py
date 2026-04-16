import requests

MODEL = "qwen2.5:7b"
API_URL = "http://localhost:11434/api/generate"

def generate(prompt, stream):
    try:
        response = requests.post(
            API_URL,
            json = {
                "model": MODEL,
                "prompt": prompt,
                "stream": stream
            },
            stream=stream
        )
    except requests.exceptions.ConnectionError as e:
        return {"error": "Ollama service not runnning"}

    return response

def intent_classification(text):
    prompt = f'''
    Classify the user's message into one of these intents: 'math_solve', 'study', 'command', or 'chat'.

    Message: {text}

    Rules:
    - 'math_solve': User asks to solve, calculate, find, compute, integrate, differentiate, or derive a specific problem
    - 'study': General academic questions, explanations, conceptual doubts, definitions, formulas (not asking to solve a specific problem), NOT QUESTIONS THAT ARE TO BE SOLVED OR EVALUATED
    - 'command': Direct commands like "open youtube", "set timer", "remind me"
    - 'chat': Casual conversation, greetings, small talk, how are you

    Examples:
    "Solve x² + 5x + 6 = 0" → math_solve, 0.95
    "Find the integral of ln(tan x)" → math_solve, 0.95
    "What is Newton's second law?" → study, 0.9
    "Explain quantum entanglement" → study, 0.9
    "Hi, how are you?" → chat, 0.95
    "Open YouTube" → command, 0.9

    Reply in EXACT format: intent, confidence
    Example: math_solve, 0.95'''
    
    response = generate(prompt, False)

    if isinstance(response, dict) and "error" in response:
        return {"intent": "chat", "confidence": 0.8}
    print("AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH", response.json()["response"])
    return response.json()["response"]

def message_response(message, intent, confidence, task, topic, context):
    
    prompt = ""
    if intent == "math_solve":
    
        # prompt = f'''
        # YOU ARE ASTRA, a study assistant who can give study-oriented responses as well as goofy conversational responses. the input is:
        # PROBLEM: {message}
        # topic: {topic}
        # task: {task}
        # context: {context}

        # IMPORTANT INSTRUCTIONS:
        # 1. FIRST, write step-by-step reasoning (2-3 sentences max)
        # 2. THEN, write Python code to compute the answer inside ```python ... ``` block
        # 3. Handle domain restrictions (absolute value, piecewise, etc.)

        # 4. For absolute value, piecewise, or domain problems:
        # - Solve each case separately
        # - FILTER roots by domain conditions before summing
        # - Only include roots that satisfy the original inequality
        # - Use print() for the final answer
        # 5. use sympy. Print the final answer.

        # The code MUST compute exactly what the question asks for:
        # - If question asks for "number of integers" → print the COUNT
        # - If asks for "sum of roots" → print the SUM
        # - If asks for "roots" → print the roots

        # For inequalities involving infinity or unbounded intervals:
        # - Do NOT iterate over infinite ranges
        # - Instead, use sympy's solve() and inequality solvers
        # - Example: sp.solve((x**2 - 4)/(x - 3) >= 0, x)


        # EXAMPLE FORMAT:
        # Step-by-step: Let's solve this...

        # ```python
        # import sympy as sp
        # # code here
        # print(result)
        
        # For integrals, ALWAYS write SymPy code like this:

        # import sympy as sp
        # x = sp.symbols('x')
        # result = sp.integrate(x * sp.ln(x), x)
        # print(result)

        # For definite integrals:
        # result = sp.integrate(sp.cos(2*x), (x, 0, sp.pi/2))
        # print(result)

        # Never skip the print statement.
        
        # '''
        prompt = f'''
        YOU ARE ASTRA, a study assistant who can give study-oriented responses as well as goofy conversational responses. the input is:
        PROBLEM: {message}
        topic: {topic}
        task: {task}
        context: {context}

        RULES:
        1. Write Python code inside ```python``` block
        2. Use SymPy for all math: algebra, calculus, equations, inequalities
        3. Always use print() for the final answer
        4. Keep code minimal. Let SymPy do the work.
        5. If question asks for "number of integers" → print the COUNT
        6. If asks for "sum of roots" → print the SUM
        7. f asks for "roots" → print the roots

        For inequalities involving infinity or unbounded intervals:
        8. Do NOT iterate over infinite ranges
        9. Instead, use sympy's solve() and inequality solvers
        10. Example: sp.solve((x**2 - 4)/(x - 3) >= 0, x)

        EXAMPLES:

        Algebra: Solve x² - 5x + 6 = 0
        ```python
        import sympy as sp
        x = sp.symbols('x')
        roots = sp.solve(x**2 - 5*x + 6, x)
        print(roots)

        Calculus: ∫ x ln x dx
        import sympy as sp
        x = sp.symbols('x')
        result = sp.integrate(x * sp.ln(x), x)
        print(result)

        Definite integral: ∫ cos(2x) dx from 0 to π/2
        import sympy as sp
        x = sp.symbols('x')
        result = sp.integrate(sp.cos(2*x), (x, 0, sp.pi/2))
        print(result)

        Absolute value: |x-3| + |x-5| = 4
        import sympy as sp
        x = sp.symbols('x')
        solutions = sp.solve(sp.Abs(x-3) + sp.Abs(x-5) - 4, x)
        print(solutions)

        In code blocks, final print() statements should only print the numeric or symmbolic values that are compute, not any labels or extra strings.
        for ex, print("Result", result) THIS IS WRONG, but print(result) THIS IS RIGHT
        RETURN a 2-line explanation, and then the code block.

        '''

    else:
       prompt =f'''YOU ARE ASTRA, a study assistant who can give study-oriented responses as well as goofy conversational responses. the input is:
                    message = {message}
                    context: [" {context} "]

                    ANSWER WITH RESPECT TO THE CONTEXT
                    ONLY GIVE YOUR RESPONSE, TALK AS ASTRA, NOTHING ELSE, DIRECT RESPONSE IS CRUCIAL

                '''
       print(prompt)
       
    return generate(prompt, stream=True)

def explain_steps(message):
    prompt = f'''
        YOU ARE ASTRA, a study assistant who can give study-oriented responses as well as goofy conversational responses. Generate a step-by-step solution for this problem.

        Problem: {message}

        Rules:
        - Number each step (Step 1:, Step 2:, etc.)
        - Use LaTeX for all math: $inline$ and $$display$$
        - Show formulas and substitutions

        ONLY GIVE YOUR RESPONSE, TALK AS ASTRA, NOTHING ELSE, DIRECT RESPONSE IS CRUCIAL
        
    '''
    return generate(prompt, stream=False).json()["response"]
    