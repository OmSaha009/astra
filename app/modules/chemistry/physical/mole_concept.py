from app.modules.chemistry.data.atomic_masses import ATOMIC_MASSES
from app.modules.chemistry.data.molar_masses import COMMON_MOLAR_MASSES
from math import gcd
import re
from app.modules.chemistry.physical.conversions import moles_to_mass
"""
1. molarity_to_molality
2. molality_to_molarity
3. wv_to_molarity
4. molarity_to_wv
5. mass_to_moles
6. moles_to_mass
7. molarity_to_moles
8. moles_to_molarity
"""

def oleum_free_so3(label):
    """Calculate % free SO3 in oleum"""
    return (((label - 100) * 80) / 18)

# 1. Dilution and mixing
def dilution_solver(M1=None, V1=None, M2=None, V2=None):
    """
    Solves M1V1 = M2V2
    Exactly ONE variable must be None.
    """

    values = [M1, V1, M2, V2]
    
    if values.count(None) != 1:
        raise ValueError("Exactly one variable must be None")

    if M1 is None:
        return (M2 * V2) / V1

    elif V1 is None:
        return (M2 * V2) / M1

    elif M2 is None:
        return (M1 * V1) / V2

    elif V2 is None:
        return (M1 * V1) / M2

def mixing_two_solutions(M1, V1, M2, V2):
    """Final molarity when mixing two solutions"""
    total_moles = (M1 * V1) + (M2 * V2)
    total_volume = V1 + V2
    return round(total_moles / total_volume, 3)


def theoretical_yield(limiting_moles, product_coefficient, limiting_coefficient):
    """Calculate theoretical yield in moles"""
    return (limiting_moles * product_coefficient) / limiting_coefficient

# Atomic masses dictionary (add more as needed)
def atomic_mass(element):
    """Get atomic mass of an element"""
    element = element.strip().capitalize()
    if element in ATOMIC_MASSES:
        return ATOMIC_MASSES[element]
    raise ValueError(f"Atomic mass for {element} not found")

def calculate_molar_mass(formula):
    """
    Calculate molar mass from chemical formula
    Example: 'H2O' -> 18.015, 'NaCl' -> 58.44
    """
    # Handle parentheses (simplified - works for simple formulas)
    # Pattern: element followed by optional number, or (group) followed by number
    pattern = r'([A-Z][a-z]?)(\d*)|\(([^()]+)\)(\d*)'
    
    total_mass = 0
    for match in re.finditer(pattern, formula):
        if match.group(1):  # Single element
            element = match.group(1)
            count = int(match.group(2)) if match.group(2) else 1
            total_mass += atomic_mass(element) * count
        elif match.group(3):  # Group in parentheses
            group_formula = match.group(3)
            multiplier = int(match.group(4)) if match.group(4) else 1
            total_mass += calculate_molar_mass(group_formula) * multiplier
    
    return round(total_mass, 3)

def formula_from_ratios(ratios):
    """
    Convert element ratios to empirical formula string
    ratios: {'C': 1, 'H': 2, 'O': 1} -> 'CH2O'
    """
    formula = ""
    # Sort elements for consistent output
    for element in sorted(ratios.keys()):
        count = ratios[element]
        if count == 1:
            formula += element
        elif count > 1:
            formula += f"{element}{count}"
    return formula

def multiply_formula(formula, n):
    """
    Multiply a chemical formula by an integer n
    Example: 'CH2O', 6 -> 'C6H12O6'
    """
    if n == 1:
        return formula
    
    pattern = r'([A-Z][a-z]?)(\d*)'
    result = ""
    
    for match in re.finditer(pattern, formula):
        element = match.group(1)
        count = int(match.group(2)) if match.group(2) else 1
        new_count = count * n
        result += f"{element}{new_count}" if new_count > 1 else element
    
    return result

# Now the working empirical/molecular formula functions
def empirical_formula(elements_dict):
    """
    elements_dict: {'C': 40, 'H': 6.67, 'O': 53.33} (percentages)
    Returns empirical formula
    """
    # Convert percentages to moles
    moles = {}
    for element, percentage in elements_dict.items():
        moles[element] = percentage / atomic_mass(element)
    
    # Find smallest mole value
    min_mole = min(moles.values())
    
    # Calculate ratios
    ratios = {}
    for element, mole_value in moles.items():
        ratio = mole_value / min_mole
        # Round to nearest integer, handle floating point precision
        rounded = round(ratio)
        # If rounding causes issues (e.g., 1.33 should be 4/3), try to find fraction
        if abs(ratio - rounded) > 0.1:
            # Try common fractions
            for denominator in [2, 3, 4]:
                candidate = round(ratio * denominator) / denominator
                if abs(ratio - candidate) < 0.05:
                    rounded = round(ratio * denominator)
                    # Multiply all ratios by denominator
                    for e in moles:
                        ratios[e] = round((moles[e] / min_mole) * denominator)
                    return formula_from_ratios(ratios)
        
        ratios[element] = rounded
    
    return formula_from_ratios(ratios)

def molecular_formula(empirical_formula_str, molar_mass):
    """Find molecular formula from empirical formula"""
    emp_mass = calculate_molar_mass(empirical_formula_str)
    n = round(molar_mass / emp_mass)
    return multiply_formula(empirical_formula_str, n)

# Additional helper for parsing compound formulas
def parse_compound(formula):
    """
    Parse a chemical formula into element counts
    Example: 'H2SO4' -> {'H': 2, 'S': 1, 'O': 4}
    """
    element_counts = {}
    pattern = r'([A-Z][a-z]?)(\d*)'
    
    for match in re.finditer(pattern, formula):
        element = match.group(1)
        count = int(match.group(2)) if match.group(2) else 1
        element_counts[element] = element_counts.get(element, 0) + count
    
    return element_counts

# 5. Solution preparation calculations
def volume_for_target_moles(target_moles, stock_M):
    """Volume needed from stock solution"""
    return round(target_moles / stock_M, 3)

def mass_for_target_M(target_M, volume_L, molar_mass):
    """Mass of solute needed for target molarity"""
    moles = target_M * volume_L
    return moles_to_mass(moles, molar_mass)

# 6. Colligative properties
def boiling_point_elevation(m, kb, i=1):
    """ΔTb = i * kb * m"""
    return round(i * kb * m, 3)

def freezing_point_depression(m, kf, i=1):
    """ΔTf = i * kf * m"""
    return round(i * kf * m, 3)

def osmotic_pressure(M, T_kelvin, i=1, R=0.0821):
    """π = i * M * R * T (in atm)"""
    return round(i * M * R * T_kelvin, 3)

# 7. Percentage calculations
def percent_yield(actual_yield, theoretical_yield):
    return round((actual_yield / theoretical_yield) * 100, 2)

def percent_error(experimental, theoretical):
    return round(abs((experimental - theoretical) / theoretical) * 100, 2)

def mass_by_volume(mass_g, volume_ml):
    """(w/v)%"""
    return round((mass_g / volume_ml) * 100, 2)

# 8. Gas stoichiometry (ideal gas law)
def moles_from_ideal_gas(P_atm, V_L, T_K, R=0.0821):
    return round((P_atm * V_L) / (R * T_K), 3)

def volume_from_ideal_gas(moles, T_K, P_atm, R=0.0821):
    return round((moles * R * T_K) / P_atm, 2)

def get_molar_mass(compound):
    """Lookup or calculate molar mass"""
    if compound in COMMON_MOLAR_MASSES:
        return COMMON_MOLAR_MASSES[compound]
    # Add calculation from formula here
    return None

def count_atoms(formula, element):
    """Count atoms in a formula (simplified)"""
    import re
    pattern = f"{element}(\\d*)"
    matches = re.findall(pattern, formula)
    total = 0
    for match in matches:
        total += int(match) if match else 1
    return total

def count_oh_groups(formula):
    """Count OH groups in a formula"""
    import re
    oh_matches = re.findall(r'OH(\d*)', formula)
    total = 0
    for match in oh_matches:
        total += int(match) if match else 1
    return total

def calculate_total_charge(formula):
    """Calculate total charge from formula (simplified)"""
    # This is complex - better to use a lookup table for common salts
    common_salts = {
        'NaCl': 1, 'Na2SO4': 2, 'Al2(SO4)3': 6,
        'CaCO3': 2, 'FeCl3': 3, 'FeCl2': 2
    }
    return common_salts.get(formula, 1)

def solve_wv_density(wv_percent, density, solvent_mass):
    """
    Solve for solute mass when:
    - w/v% is given
    - density is given
    - solvent mass is given
    """
    
    import sympy as sp
    
    x = sp.symbols('x')

    volume = (solvent_mass + x) / density
    
    equation = (x / volume) * 100 - wv_percent
    
    sol = sp.solve(equation, x)
    
    return float(sol[0])