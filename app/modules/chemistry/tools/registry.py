from ..physical.conversions import (
    molarity_to_molality,
    molality_to_molarity,
    wv_to_molarity,
    molarity_to_wv,
    mass_to_moles,
    moles_to_mass,
    molarity_to_moles,
    moles_to_molarity,
    molarity_to_normality,
    normality_to_molarity,
    molarity_to_strength,
    ww_to_molarity,
    molarity_to_ww,
    molality_to_mole_fraction,
    ppm_to_molarity,
    molarity_to_ppm,
    ppm_element_to_compound_mass
)
from ..physical.mole_concept import (
    oleum_free_so3,
    dilution_solver,
    mixing_two_solutions,
    theoretical_yield,
    atomic_mass,
    calculate_molar_mass,
    formula_from_ratios,
    multiply_formula,
    empirical_formula,
    molecular_formula,
    parse_compound,
    volume_for_target_moles,
    mass_for_target_M,
    boiling_point_elevation,
    freezing_point_depression,
    osmotic_pressure,
    percent_yield,
    percent_error,
    mass_by_volume,
    moles_from_ideal_gas,
    volume_from_ideal_gas,
    get_molar_mass,
    count_atoms,
    count_oh_groups,
    calculate_total_charge,
    solve_wv_density
)

from ..physical.stoichiometry import (
    parse_formula,
    balance_equation,
    format_balanced_equation,
    limiting_reagent
)

from ..physical.redox import (
    get_n_factor,
    calculate_redox_nfactor,
    auto_detect_nfactor
)

TOOLS = {
    # ========== CONVERSIONS ==========
    "molarity_to_molality": {
        "function": molarity_to_molality,
        "args": ["molar_mass", "density", "M"],
        "returns": "molality",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert molarity to molality using density and molar mass"
    },
    "molality_to_molarity": {
        "function": molality_to_molarity,
        "args": ["molar_mass", "density", "m"],
        "returns": "molarity",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert molality to molarity using density and molar mass"
    },
    "wv_to_molarity": {
        "function": wv_to_molarity,
        "args": ["wv_percent", "molar_mass"],
        "returns": "molarity",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert w/v% to molarity"
    },
    "molarity_to_wv": {
        "function": molarity_to_wv,
        "args": ["M", "molar_mass"],
        "returns": "wv_percent",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert molarity to w/v%"
    },
    "mass_to_moles": {
        "function": mass_to_moles,
        "args": ["mass", "molar_mass"],
        "returns": "moles",
        "tags": ["mole_concept", "conversion"],
        "category": "mole_concept",
        "description": "Convert mass (g) to moles"
    },
    "moles_to_mass": {
        "function": moles_to_mass,
        "args": ["moles", "molar_mass"],
        "returns": "mass",
        "tags": ["mole_concept", "conversion"],
        "category": "mole_concept",
        "description": "Convert moles to mass (g)"
    },
    "molarity_to_moles": {
        "function": molarity_to_moles,
        "args": ["M", "volume_L"],
        "returns": "moles",
        "tags": ["mole_concept", "concentration"],
        "category": "mole_concept",
        "description": "Calculate moles from molarity and volume"
    },
    "moles_to_molarity": {
        "function": moles_to_molarity,
        "args": ["moles", "volume_L"],
        "returns": "molarity",
        "tags": ["mole_concept", "concentration"],
        "category": "mole_concept",
        "description": "Calculate molarity from moles and volume"
    },
    "molarity_to_normality": {
        "function": molarity_to_normality,
        "args": ["M", "n_factor"],
        "returns": "normality",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert molarity to normality using n-factor"
    },
    "normality_to_molarity": {
        "function": normality_to_molarity,
        "args": ["N", "n_factor"],
        "returns": "molarity",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert normality to molarity using n-factor"
    },
    "molarity_to_strength": {
        "function": molarity_to_strength,
        "args": ["M", "molar_mass"],
        "returns": "strength",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert molarity to strength (g/L)"
    },
    "ww_to_molarity": {
        "function": ww_to_molarity,
        "args": ["w_w", "density", "molar_mass"],
        "returns": "molarity",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert w/w% to molarity using density"
    },
    "molarity_to_ww": {
        "function": molarity_to_ww,
        "args": ["M", "density", "molar_mass"],
        "returns": "ww_percent",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert molarity to w/w%"
    },
    "molality_to_mole_fraction": {
        "function": molality_to_mole_fraction,
        "args": ["m", "solvent_molar_mass"],
        "returns": "mole_fraction",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert molality to mole fraction of solute"
    },
    "ppm_to_molarity": {
        "function": ppm_to_molarity,
        "args": ["ppm", "molar_mass", "density"],
        "returns": "molarity",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert ppm to molarity"
    },
    "molarity_to_ppm": {
        "function": molarity_to_ppm,
        "args": ["M", "molar_mass"],
        "returns": "ppm",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert molarity to ppm"
    },
    "ppm_element_to_compound_mass": {
        "function": ppm_element_to_compound_mass,
        "args": ["element_ppm", "element_molar_mass", "compound_molar_mass"],
        "returns": "compound_ppm",
        "tags": ["concentration", "conversion"],
        "category": "conversions",
        "description": "Convert ppm of element to ppm of compound"
    },

    # ========== MOLE CONCEPT ==========
    "oleum_free_so3": {
        "function": oleum_free_so3,
        "args": ["label"],
        "returns": "free_so3_percent",
        "tags": ["mole_concept", "oleum"],
        "category": "mole_concept",
        "description": "Calculate % free SO3 in oleum"
    },
    "dilution_solver": {
        "function": dilution_solver,
        "args": ["M1", "V1", "V2"],
        "returns": "M2",
        "tags": ["concentration", "dilution"],
        "category": "mole_concept",
        "description": "Solve M1V1 = M2V2 dilution problems"
    },
    "mixing_two_solutions": {
        "function": mixing_two_solutions,
        "args": ["M1", "V1", "M2", "V2"],
        "returns": "M_final",
        "tags": ["concentration", "mixing"],
        "category": "mole_concept",
        "description": "Calculate final concentration when mixing two solutions"
    },
    "theoretical_yield": {
        "function": theoretical_yield,
        "args": ["limiting_moles", "product_coefficient", "limiting_coefficient"],
        "returns": "yield_moles",
        "tags": ["stoichiometry", "yield"],
        "category": "stoichiometry",
        "description": "Calculate theoretical yield in moles"
    },
    "atomic_mass": {
        "function": atomic_mass,
        "args": ["element"],
        "returns": "mass",
        "tags": ["periodic", "atomic"],
        "category": "periodic",
        "description": "Get atomic mass of an element"
    },
    "calculate_molar_mass": {
        "function": calculate_molar_mass,
        "args": ["formula"],
        "returns": "molar_mass",
        "tags": ["mole_concept", "formula"],
        "category": "mole_concept",
        "description": "Calculate molar mass from chemical formula"
    },
    "empirical_formula": {
        "function": empirical_formula,
        "args": ["elements_dict"],
        "returns": "formula",
        "tags": ["mole_concept", "formula"],
        "category": "mole_concept",
        "description": "Determine empirical formula from percentage composition"
    },
    "molecular_formula": {
        "function": molecular_formula,
        "args": ["empirical_formula_str", "molar_mass"],
        "returns": "formula",
        "tags": ["mole_concept", "formula"],
        "category": "mole_concept",
        "description": "Determine molecular formula from empirical formula and molar mass"
    },
    "multiply_formula": {
        "function": multiply_formula,
        "args": ["formula", "n"],
        "returns": "formula",
        "tags": ["mole_concept", "formula"],
        "category": "mole_concept",
        "description": "Multiply a chemical formula by an integer"
    },
    "formula_from_ratios": {
        "function": formula_from_ratios,
        "args": ["ratios"],
        "returns": "formula",
        "tags": ["mole_concept", "formula"],
        "category": "mole_concept",
        "description": "Convert element ratios to formula string"
    },
    "parse_compound": {
        "function": parse_compound,
        "args": ["formula"],
        "returns": "element_counts",
        "tags": ["mole_concept", "formula"],
        "category": "mole_concept",
        "description": "Parse compound formula into element counts"
    },
    "volume_for_target_moles": {
        "function": volume_for_target_moles,
        "args": ["target_moles", "stock_M"],
        "returns": "volume",
        "tags": ["concentration", "dilution"],
        "category": "mole_concept",
        "description": "Calculate volume needed from stock solution"
    },
    "mass_for_target_M": {
        "function": mass_for_target_M,
        "args": ["target_M", "volume_L", "molar_mass"],
        "returns": "mass",
        "tags": ["concentration", "preparation"],
        "category": "mole_concept",
        "description": "Calculate mass of solute needed for target molarity"
    },
    "solve_wv_density": {
        "function": solve_wv_density,
        "args": ["solvent_mass", "density", "w_v_percent"],
        "returns": "solute_mass",
        "tags": ["concentration", "wv"],
        "category": "mole_concept",
        "description": "Solve for solute mass given w/v%, solvent mass, density"
    },

    # ========== COLLIGATIVE PROPERTIES ==========
    "boiling_point_elevation": {
        "function": boiling_point_elevation,
        "args": ["m", "kb", "i"],
        "returns": "delta_Tb",
        "tags": ["colligative", "boiling_point"],
        "category": "colligative",
        "description": "Calculate boiling point elevation ΔTb = i × kb × m"
    },
    "freezing_point_depression": {
        "function": freezing_point_depression,
        "args": ["m", "kf", "i"],
        "returns": "delta_Tf",
        "tags": ["colligative", "freezing_point"],
        "category": "colligative",
        "description": "Calculate freezing point depression ΔTf = i × kf × m"
    },
    "osmotic_pressure": {
        "function": osmotic_pressure,
        "args": ["M", "T_kelvin", "i", "R"],
        "returns": "pressure_atm",
        "tags": ["colligative", "osmotic_pressure"],
        "category": "colligative",
        "description": "Calculate osmotic pressure π = i × M × R × T"
    },

    # ========== YIELD & ERROR ==========
    "percent_yield": {
        "function": percent_yield,
        "args": ["actual_yield", "theoretical_yield"],
        "returns": "percent",
        "tags": ["stoichiometry", "yield"],
        "category": "stoichiometry",
        "description": "Calculate percent yield"
    },
    "percent_error": {
        "function": percent_error,
        "args": ["experimental", "theoretical"],
        "returns": "percent",
        "tags": ["measurement", "error"],
        "category": "general",
        "description": "Calculate percent error"
    },
    "mass_by_volume": {
        "function": mass_by_volume,
        "args": ["mass_g", "volume_ml"],
        "returns": "wv_percent",
        "tags": ["concentration", "wv"],
        "category": "conversions",
        "description": "Calculate (w/v)% from mass and volume"
    },

    # ========== GAS STOICHIOMETRY ==========
    "moles_from_ideal_gas": {
        "function": moles_from_ideal_gas,
        "args": ["P_atm", "V_L", "T_K", "R"],
        "returns": "moles",
        "tags": ["gas", "stoichiometry"],
        "category": "gas",
        "description": "Calculate moles using ideal gas law PV = nRT"
    },
    "volume_from_ideal_gas": {
        "function": volume_from_ideal_gas,
        "args": ["moles", "T_K", "P_atm", "R"],
        "returns": "volume",
        "tags": ["gas", "stoichiometry"],
        "category": "gas",
        "description": "Calculate volume using ideal gas law"
    },
    "get_molar_mass": {
        "function": get_molar_mass,
        "args": ["compound"],
        "returns": "molar_mass",
        "tags": ["mole_concept", "periodic"],
        "category": "mole_concept",
        "description": "Lookup or calculate molar mass of common compound"
    },

    # ========== STOICHIOMETRY ==========
    "parse_formula": {
        "function": parse_formula,
        "args": ["formula"],
        "returns": "element_counts",
        "tags": ["stoichiometry", "formula"],
        "category": "stoichiometry",
        "description": "Parse chemical formula into element counts"
    },
    "balance_equation": {
        "function": balance_equation,
        "args": ["reactants", "products"],
        "returns": "coefficients",
        "tags": ["stoichiometry", "balancing"],
        "category": "stoichiometry",
        "description": "Balance a chemical equation using matrix method"
    },
    "format_balanced_equation": {
        "function": format_balanced_equation,
        "args": ["reactants", "products", "coefficients"],
        "returns": "equation_string",
        "tags": ["stoichiometry", "balancing"],
        "category": "stoichiometry",
        "description": "Format balanced equation as readable string"
    },
    "limiting_reagent": {
        "function": limiting_reagent,
        "args": ["moles_dict", "coefficients_dict"],
        "returns": "limiting_reactant",
        "tags": ["stoichiometry", "limiting_reagent"],
        "category": "stoichiometry",
        "description": "Determine limiting reagent from moles and coefficients"
    },

    # ========== REDOX ==========
    "get_n_factor": {
        "function": get_n_factor,
        "args": ["compound", "reaction_type", "medium"],
        "returns": "n_factor",
        "tags": ["redox", "normality"],
        "category": "redox",
        "description": "Get n-factor for acids, bases, salts, redox reactions"
    },
    "calculate_redox_nfactor": {
        "function": calculate_redox_nfactor,
        "args": ["element", "from_state", "to_state"],
        "returns": "n_factor",
        "tags": ["redox", "normality"],
        "category": "redox",
        "description": "Calculate n-factor for redox reactions"
    },
    "count_atoms": {
    "function": count_atoms,
    "args": ["formula", "element"],
    "returns": "count",
    "tags": ["stoichiometry", "formula"],
    "category": "stoichiometry",
    "description": "Count number of atoms of a specific element in a formula"
    },
    "count_oh_groups": {
        "function": count_oh_groups,
        "args": ["formula"],
        "returns": "count",
        "tags": ["stoichiometry", "formula", "acid_base"],
        "category": "stoichiometry",
        "description": "Count number of OH groups in a formula"
    },
    "calculate_total_charge": {
        "function": calculate_total_charge,
        "args": ["formula"],
        "returns": "charge",
        "tags": ["stoichiometry", "ionic", "redox"],
        "category": "stoichiometry",
        "description": "Calculate total charge of a compound or ion from formula"
    },
    "auto_detect_nfactor": {
        "function": auto_detect_nfactor,
        "args": ["formula"],
        "returns": "n_factor",
        "tags": ["redox", "normality", "acid_base"],
        "category": "redox",
        "description": "Automatically detect n-factor from chemical formula"
    }
}


def get_tools_by_tags(tags: list) -> dict:
    filtered = {}
    for name, tool in TOOLS.items():
        if any(tag in tool["tags"] for tag in tags):
            filtered[name] = tool

    return filtered