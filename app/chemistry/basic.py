from math import gcd
import re

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



def molarity_to_molality(molar_mass, density, molarity):
    m = (1000 * molarity)/(1000*density - molarity*molar_mass)
    m = round(m, 3)

    return m

def molality_to_molarity(molar_mass, density, molality):
    m = (1000*molality*density)/(1000 + molar_mass*molality)
    m = round(m, 3)
    return m

def wv_to_molarity(wv_percent, molar_mass):
    mass_solute_g = wv_percent
    moles_solute = mass_solute_g/molar_mass
    m = (moles_solute/100)*1000
    m = round(m,3)
    return m

def molarity_to_wv(molarity, molar_mass):
    mass_solute = molarity * molar_mass
    volume = 1000
    wv = (mass_solute/volume)*100
    wv = round(wv, 3)
    return wv

def mass_to_moles(mass_g, molar_mass):
    return round( mass_g/molar_mass ,3)

def moles_to_mass(moles, molar_mass):
    return round(moles * molar_mass, 3)


def molarity_to_moles(M, volume_L):
    return round(M * volume_L, 3)


def moles_to_molarity(moles, volume_L):
    return round(moles / volume_L, 3)

def molarity_to_normality(M, n_factor):
    return M * n_factor

def normality_to_molarity(N, n_factor):
    return N / n_factor

def molarity_to_strength(M, molar_mass):
    return M * molar_mass

def ww_to_molarity(w_w, density, molar_mass):
    """w/w% to Molarity"""
    return (10 * density * w_w) / molar_mass

def molarity_to_ww(M, density, molar_mass):
    """Molarity to w/w%"""
    return (M * molar_mass) / (10 * density)

def molality_to_mole_fraction(m, solvent_molar_mass=18):
    """Molality to mole fraction of solute in water"""
    return m / (m + 1000/solvent_molar_mass)

def oleum_free_so3(label):
    """Calculate % free SO3 in oleum"""
    return (label - 100) * 100 / 80

# 1. Dilution and mixing
def dilution(M1, V1, V2):
    """M1V1 = M2V2"""
    return round(M1 * V1 / V2, 3)

def mixing_two_solutions(M1, V1, M2, V2):
    """Final molarity when mixing two solutions"""
    total_moles = (M1 * V1) + (M2 * V2)
    total_volume = V1 + V2
    return round(total_moles / total_volume, 3)

# 2. Concentration conversions
def ppm_to_molarity(ppm, molar_mass, density=1):
    """ppm to Molarity (assuming dilute aqueous)"""
    return round((ppm / molar_mass) / 1000, 6)

def molarity_to_ppm(M, molar_mass):
    """Molarity to ppm"""
    return round(M * molar_mass * 1000, 2)

# 3. Stoichiometry helpers
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

def theoretical_yield(limiting_moles, product_coefficient, limiting_coefficient):
    """Calculate theoretical yield in moles"""
    return (limiting_moles * product_coefficient) / limiting_coefficient

# Atomic masses dictionary (add more as needed)
ATOMIC_MASSES = {
    # Period 1
    'H': 1.008, 'He': 4.0026,
    
    # Period 2
    'Li': 6.94, 'Be': 9.012, 'B': 10.81, 'C': 12.011, 'N': 14.007,
    'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    
    # Period 3
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
    'S': 32.06, 'Cl': 35.45, 'Ar': 39.95,
    
    # Period 4
    'K': 39.098, 'Ca': 40.078, 'Sc': 44.956, 'Ti': 47.867, 'V': 50.942,
    'Cr': 51.996, 'Mn': 54.938, 'Fe': 55.845, 'Co': 58.933, 'Ni': 58.693,
    'Cu': 63.546, 'Zn': 65.38, 'Ga': 69.723, 'Ge': 72.630, 'As': 74.922,
    'Se': 78.971, 'Br': 79.904, 'Kr': 83.798,
    
    # Period 5
    'Rb': 85.468, 'Sr': 87.62, 'Y': 88.906, 'Zr': 91.224, 'Nb': 92.906,
    'Mo': 95.95, 'Tc': 98.00, 'Ru': 101.07, 'Rh': 102.91, 'Pd': 106.42,
    'Ag': 107.87, 'Cd': 112.41, 'In': 114.82, 'Sn': 118.71, 'Sb': 121.76,
    'Te': 127.60, 'I': 126.90, 'Xe': 131.29,
    
    # Period 6
    'Cs': 132.91, 'Ba': 137.33, 'La': 138.91, 'Ce': 140.12, 'Pr': 140.91,
    'Nd': 144.24, 'Pm': 145.00, 'Sm': 150.36, 'Eu': 151.96, 'Gd': 157.25,
    'Tb': 158.93, 'Dy': 162.50, 'Ho': 164.93, 'Er': 167.26, 'Tm': 168.93,
    'Yb': 173.05, 'Lu': 174.97, 'Hf': 178.49, 'Ta': 180.95, 'W': 183.84,
    'Re': 186.21, 'Os': 190.23, 'Ir': 192.22, 'Pt': 195.08, 'Au': 196.97,
    'Hg': 200.59, 'Tl': 204.38, 'Pb': 207.2, 'Bi': 208.98, 'Po': 209.00,
    'At': 210.00, 'Rn': 222.00,
    
    # Period 7 (only those relevant for JEE)
    'Fr': 223.00, 'Ra': 226.00, 'Ac': 227.00, 'Th': 232.04, 'Pa': 231.04,
    'U': 238.03, 'Np': 237.00, 'Pu': 244.00
    
    # Note: 'N' appears twice in your original (14.007), kept as is
}
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

# 9. Common constants lookup
COMMON_MOLAR_MASSES = {
    'H2O': 18.015, 'NaCl': 58.44, 'NaOH': 40.00, 'HCl': 36.46,
    'H2SO4': 98.079, 'HNO3': 63.01, 'CH3COOH': 60.052,
    'NH3': 17.031, 'CO2': 44.01, 'CaCO3': 100.09
}

def get_molar_mass(compound):
    """Lookup or calculate molar mass"""
    if compound in COMMON_MOLAR_MASSES:
        return COMMON_MOLAR_MASSES[compound]
    # Add calculation from formula here
    return None

def get_n_factor(compound, reaction_type=None, **kwargs):
    """
    Retrieve n-factor for various compounds and reactions.
    
    Args:
        compound: str or dict - compound name/formula
        reaction_type: str - 'acid', 'base', 'redox', 'salt', 'complexation'
        **kwargs: additional params like 'product', 'oxidation_states'
    """
    
    # Predefined n-factors for common scenarios
    n_factor_db = {
        # Acids (basicity)
        'HCl': 1, 'HNO3': 1, 'CH3COOH': 1,
        'H2SO4': 2, 'H2CO3': 2, 'H2S': 2,
        'H3PO4': 3, 'H3PO3': 2,  # Phosphorous acid
        'H3PO2': 1,  # Hypophosphorous acid
        
        # Bases (acidity)
        'NaOH': 1, 'KOH': 1, 'NH4OH': 1,
        'Ca(OH)2': 2, 'Mg(OH)2': 2, 'Al(OH)3': 3,
        
        # Common redox agents
        'KMnO4': {'acidic': 5, 'neutral': 3, 'basic': 1},
        'K2Cr2O7': {'acidic': 6},
        'H2O2': {'oxidizing': 2, 'reducing': 2},
        'Na2S2O3': 1,  # With iodine
        'FeSO4': 1, 'FeC2O4': 3,
        'KIO3': {'acidic': 5, 'neutral': 6},
        
        # Salts (total cationic/anionic charge)
        'NaCl': 1, 'CaCl2': 2, 'AlCl3': 3,
        'Na2CO3': 2, 'Na3PO4': 3,
    }
    
    # Handle redox with oxidation state calculation
    if reaction_type == 'redox' or compound in ['KMnO4', 'K2Cr2O7']:
        if compound == 'KMnO4':
            return n_factor_db['KMnO4'].get(kwargs.get('medium', 'acidic'), 5)
        elif compound == 'K2Cr2O7':
            return 6
        elif 'element' in kwargs and 'product' in kwargs:
            return calculate_redox_nfactor(kwargs['element'], kwargs['oxidation_state_from'], 
                                          kwargs['oxidation_state_to'])
    
    # For acids/bases
    if reaction_type in ['acid', 'base']:
        return n_factor_db.get(compound, 1)
    
    # Direct lookup
    if compound in n_factor_db:
        return n_factor_db[compound]
    
    # Auto-detect from formula
    return auto_detect_nfactor(compound)

def calculate_redox_nfactor(element, from_state, to_state):
    """Calculate n-factor for redox reactions"""
    return abs(to_state - from_state)

def auto_detect_nfactor(formula):
    """Automatically detect n-factor from chemical formula"""
    # Count replaceable H+ in acids
    if formula.startswith('H') and len(formula) > 1:
        h_count = count_atoms(formula, 'H')
        if h_count > 0:
            return h_count
    
    # Count OH- in bases
    if 'OH' in formula:
        oh_count = count_oh_groups(formula)
        if oh_count > 0:
            return oh_count
    
    # For salts, calculate total positive/negative charge
    charge = calculate_total_charge(formula)
    if charge != 0:
        return abs(charge)
    
    return 1  # default

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

if __name__ == "__main__":
    # Test 1: Molarity ↔ Molality
    print("Test 1: Molarity to Molality")
    print(f"  2M H2SO4, density 1.2, molar mass 98 → {molarity_to_molality(98, 1.2, 2)} m")
    
    print("\nTest 2: w/v% to Molarity")
    print(f"  10% w/v glucose, M=180 → {wv_to_molarity(10, 180)} M")
    
    print("\nTest 3: Empirical formula from percentages")
    print(f"  C=40%, H=6.67%, O=53.33% → {empirical_formula({'C': 40, 'H': 6.67, 'O': 53.33})}")
    
    print("\nTest 4: Molecular formula")
    print(f"  Empirical CH2O, molar mass 180 → {molecular_formula('CH2O', 180)}")
    
    print("\nTest 5: Molar mass from formula")
    print(f"  H2SO4 → {calculate_molar_mass('H2SO4')} g/mol")
    
    print("\nTest 6: Limiting reagent")
    moles = {'H2': 3, 'O2': 2}
    coeff = {'H2': 2, 'O2': 1}
    print(f"  H2: 3 mol, O2: 2 mol, 2H2 + O2 → 2H2O")
    print(f"  Limiting reagent: {limiting_reagent(moles, coeff)}")