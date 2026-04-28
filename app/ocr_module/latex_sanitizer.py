import re

class LatexSanitizer:
    def __init__(self):
        self.for_sympy = [
            (r'\blambda\b', 'lam'),           
            (r'\bβ\b', 'beta'),               
            (r'\bα\b', 'alpha'),
            (r'\bγ\b', 'gamma'),
            (r'\bθ\b', 'theta'),
        ]
        
        self.for_display = [
            (r'lam', r'\\lambda'),            
            (r'\\log', r'\\operatorname{ln}'),
            (r'beta', r'\\beta'),             
            (r'alpha', r'\\alpha'),
            (r'gamma', r'\\gamma'),
            (r'theta', r'\\theta'),
        ]

    def sanitize_for_sympy(self, expr_str: str) -> str:
        result = expr_str
        for pattern, replacement in self.for_sympy:
            result = re.sub(pattern, replacement, result)
        return result

    def sanitize_for_display(self, latex_str: str) -> str:
        result = latex_str
        for pattern, replacement in self.for_display:
            result = re.sub(pattern, replacement, result)
        return result
    
    def process_result(self, result_str: str) -> str:
        safe_for_sympy = self.sanitize_for_sympy(result_str)
        
        import sympy as sp
        expr = sp.sympify(safe_for_sympy)
        latex = sp.latex(expr)
        display_latex = self.sanitize_for_display(latex)
        return display_latex