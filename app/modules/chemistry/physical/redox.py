from app.modules.chemistry.physical.mole_concept import count_atoms, count_oh_groups, calculate_total_charge


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