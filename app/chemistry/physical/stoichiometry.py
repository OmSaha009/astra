# modules/chemistry/physical/stoichiometry.py

import re
from sympy import Matrix, lcm
from collections import defaultdict

def parse_formula(formula: str) -> dict:
    """
    Parse a chemical formula into element counts.
    Example: 'H2SO4' -> {'H': 2, 'S': 1, 'O': 4}
    Supports parentheses: 'Ca(OH)2' -> {'Ca': 1, 'O': 2, 'H': 2}
    """
    element_counts = defaultdict(float)
    
    # Handle parentheses recursively
    while '(' in formula:
        match = re.search(r'\(([^()]+)\)(\d*)', formula)
        if not match:
            break
        inside, multiplier = match.groups()
        multiplier = int(multiplier) if multiplier else 1
        # Parse inside
        inner_counts = parse_formula(inside)
        for elem, count in inner_counts.items():
            element_counts[elem] += count * multiplier
        # Remove the processed part
        formula = formula[:match.start()] + formula[match.end():]
    
    # Parse simple elements
    pattern = r'([A-Z][a-z]?)(\d*)'
    for match in re.finditer(pattern, formula):
        element = match.group(1)
        count = int(match.group(2)) if match.group(2) else 1
        element_counts[element] += count
    
    return dict(element_counts)


def balance_equation(reactants: list, products: list) -> dict:
    """
    Balance a chemical equation using matrix method.
    
    Example:
    balance_equation(['H2', 'O2'], ['H2O'])
    Returns: {'H2': 2, 'O2': 1, 'H2O': 2}
    """
    # Get all unique elements
    elements = set()
    all_compounds = reactants + products
    
    for compound in all_compounds:
        elements.update(parse_formula(compound).keys())
    elements = sorted(elements)
    
    # Build coefficient matrix: each element gives one equation
    # For each compound: coefficient appears in equation
    # For reactants: positive, products: negative
    A = []
    
    for element in elements:
        row = []
        for compound in reactants:
            counts = parse_formula(compound)
            row.append(counts.get(element, 0))
        for compound in products:
            counts = parse_formula(compound)
            row.append(-counts.get(element, 0))
        A.append(row)
    
    # Convert to SymPy Matrix and find null space
    A_matrix = Matrix(A)
    nullspace = A_matrix.nullspace()
    
    if not nullspace:
        return {"error": "Could not balance equation"}
    
    # Get the first solution
    solution = nullspace[0]
    
    # Convert to smallest integers
    coeffs = [abs(int(round(c))) for c in solution]
    
    # Find LCM to scale if needed
    from math import gcd
    lcm_val = 1
    for c in coeffs:
        lcm_val = lcm_val * c // gcd(lcm_val, c) if c else lcm_val
    
    # Scale coefficients
    coeffs = [c * lcm_val for c in coeffs]
    
    # Return dictionary
    result = {}
    for i, compound in enumerate(all_compounds):
        result[compound] = coeffs[i]
    
    return result


def format_balanced_equation(reactants: list, products: list, coefficients: dict) -> str:
    """Format balanced equation as string"""
    left = []
    for reactant in reactants:
        coeff = coefficients.get(reactant, 1)
        left.append(f"{coeff}{reactant}" if coeff != 1 else reactant)
    
    right = []
    for product in products:
        coeff = coefficients.get(product, 1)
        right.append(f"{coeff}{product}" if coeff != 1 else product)
    
    return " + ".join(left) + " → " + " + ".join(right)

def limiting_reagent(moles_dict, coefficients_dict):
    """
    Find limiting reagent
    moles_dict: {'A': 2, 'B': 3}
    coefficients_dict: {'A': 1, 'B': 2}
    """
    ratios = {}
    for reactant in moles_dict:
        ratios[reactant] = moles_dict[reactant] / coefficients_dict[reactant]
    return min(ratios, key=ratios.get)

# # Test
# if __name__ == "__main__":
#     # Test 1: H2 + O2 -> H2O
#     result = balance_equation(['H2', 'O2'], ['H2O'])
#     print(result)
#     print(format_balanced_equation(['H2', 'O2'], ['H2O'], result))
    
#     # Test 2: Fe + O2 -> Fe2O3
#     result = balance_equation(['Fe', 'O2'], ['Fe2O3'])
#     print(format_balanced_equation(['Fe', 'O2'], ['Fe2O3'], result))
    
#     # Test 3: C6H12O6 + O2 -> CO2 + H2O
#     result = balance_equation(['C6H12O6', 'O2'], ['CO2', 'H2O'])
#     print(result)