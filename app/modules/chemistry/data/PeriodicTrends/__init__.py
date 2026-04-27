"""
Unified data access layer for all element properties.
Imports from all block, group, and period files.
"""

import re
from typing import Dict, Any, Optional

from app.modules.chemistry.data.PeriodicTrends.Blocks import d_block, f_block, p_block
from app.modules.chemistry.data.PeriodicTrends.Group import group_1, group_10, group_11, group_12, group_13, group_14, group_15, group_16, group_17, group_18, group_2, group_3, group_4, group_5, group_6, group_7, group_8

# ============================================================
# Master dictionary to hold all element data
# ============================================================

ELEMENT_DATA = {}

# Mapping from symbol to full name (for lookup)
SYMBOL_TO_NAME = {}
NAME_TO_SYMBOL = {}

# ============================================================
# Helper to parse element names like "Oxygen (O)"
# ============================================================

def parse_element_name(name: str) -> tuple:
    """Parse 'Oxygen (O)' -> ('O', 'Oxygen')"""
    match = re.match(r'(.+?)\s*\(([A-Z][a-z]?)\)', name)
    if match:
        full_name, symbol = match.groups()
        return symbol, full_name.strip()
    return name, name


# ============================================================
# Import data from your files
# ============================================================

# Import Group data
from app.modules.chemistry.data.PeriodicTrends.Group import group_9

# Import Block data  
from app.modules.chemistry.data.PeriodicTrends.Blocks import s_block

# Import Period data (if you have)
# from chemistry.data.Period import period_2, period_3, etc.


def load_data_from_dict(data_dict: Dict[str, Any], property_name: str):
    """Load data from a dictionary into ELEMENT_DATA"""
    for name, value in data_dict.items():
        symbol, full_name = parse_element_name(name)
        
        if symbol not in ELEMENT_DATA:
            ELEMENT_DATA[symbol] = {
                "name": full_name,
                "symbol": symbol,
            }
            SYMBOL_TO_NAME[symbol] = full_name
            NAME_TO_SYMBOL[full_name] = symbol
        
        ELEMENT_DATA[symbol][property_name] = value


# Load all your data
# Groups

load_data_from_dict(group_1.electronegativity, "electronegativity")
load_data_from_dict(group_1.atomic_radii, "atomic_radius")
load_data_from_dict(group_1.density, "density")
load_data_from_dict(group_1.melting_point, "melting_point")
load_data_from_dict(group_1.boiling_point, "boiling_point")

load_data_from_dict(group_2.electronegativity, "electronegativity")
load_data_from_dict(group_2.atomic_radii, "atomic_radius")
load_data_from_dict(group_2.density, "density")
load_data_from_dict(group_2.melting_point, "melting_point")
load_data_from_dict(group_2.boiling_point, "boiling_point")

load_data_from_dict(group_3.electronegativity, "electronegativity")
load_data_from_dict(group_3.atomic_radii, "atomic_radius")
load_data_from_dict(group_3.density, "density")
load_data_from_dict(group_3.melting_point, "melting_point")
load_data_from_dict(group_3.boiling_point, "boiling_point")

load_data_from_dict(group_4.electronegativity, "electronegativity")
load_data_from_dict(group_4.atomic_radii, "atomic_radius")
load_data_from_dict(group_4.density, "density")
load_data_from_dict(group_4.melting_point, "melting_point")
load_data_from_dict(group_4.boiling_point, "boiling_point")

load_data_from_dict(group_5.electronegativity, "electronegativity")
load_data_from_dict(group_5.atomic_radii, "atomic_radius")
load_data_from_dict(group_5.density, "density")
load_data_from_dict(group_5.melting_point, "melting_point")
load_data_from_dict(group_5.boiling_point, "boiling_point")

load_data_from_dict(group_6.electronegativity, "electronegativity")
load_data_from_dict(group_6.atomic_radii, "atomic_radius")
load_data_from_dict(group_6.density, "density")
load_data_from_dict(group_6.melting_point, "melting_point")
load_data_from_dict(group_6.boiling_point, "boiling_point")

load_data_from_dict(group_7.electronegativity, "electronegativity")
load_data_from_dict(group_7.atomic_radii, "atomic_radius")
load_data_from_dict(group_7.density, "density")
load_data_from_dict(group_7.melting_point, "melting_point")
load_data_from_dict(group_7.boiling_point, "boiling_point")

load_data_from_dict(group_8.electronegativity, "electronegativity")
load_data_from_dict(group_8.atomic_radii, "atomic_radius")
load_data_from_dict(group_8.density, "density")
load_data_from_dict(group_8.melting_point, "melting_point")
load_data_from_dict(group_8.boiling_point, "boiling_point")

load_data_from_dict(group_9.electronegativity, "electronegativity")
load_data_from_dict(group_9.atomic_radii, "atomic_radius")
load_data_from_dict(group_9.density, "density")
load_data_from_dict(group_9.melting_point, "melting_point")
load_data_from_dict(group_9.boiling_point, "boiling_point")

load_data_from_dict(group_10.electronegativity, "electronegativity")
load_data_from_dict(group_10.atomic_radii, "atomic_radius")
load_data_from_dict(group_10.density, "density")
load_data_from_dict(group_10.melting_point, "melting_point")
load_data_from_dict(group_10.boiling_point, "boiling_point")

load_data_from_dict(group_11.electronegativity, "electronegativity")
load_data_from_dict(group_11.atomic_radii, "atomic_radius")
load_data_from_dict(group_11.density, "density")
load_data_from_dict(group_11.melting_point, "melting_point")
load_data_from_dict(group_11.boiling_point, "boiling_point")

load_data_from_dict(group_12.electronegativity, "electronegativity")
load_data_from_dict(group_12.atomic_radii, "atomic_radius")
load_data_from_dict(group_12.density, "density")
load_data_from_dict(group_12.melting_point, "melting_point")
load_data_from_dict(group_12.boiling_point, "boiling_point")

load_data_from_dict(group_13.electronegativity, "electronegativity")
load_data_from_dict(group_13.atomic_radii, "atomic_radius")
load_data_from_dict(group_13.density, "density")
load_data_from_dict(group_13.melting_point, "melting_point")
load_data_from_dict(group_13.boiling_point, "boiling_point")

load_data_from_dict(group_14.electronegativity, "electronegativity")
load_data_from_dict(group_14.atomic_radii, "atomic_radius")
load_data_from_dict(group_14.density, "density")
load_data_from_dict(group_14.melting_point, "melting_point")
load_data_from_dict(group_14.boiling_point, "boiling_point")

load_data_from_dict(group_15.electronegativity, "electronegativity")
load_data_from_dict(group_15.atomic_radii, "atomic_radius")
load_data_from_dict(group_15.density, "density")
load_data_from_dict(group_15.melting_point, "melting_point")
load_data_from_dict(group_15.boiling_point, "boiling_point")

load_data_from_dict(group_16.electronegativity, "electronegativity")
load_data_from_dict(group_16.atomic_radii, "atomic_radius")
load_data_from_dict(group_16.density, "density")
load_data_from_dict(group_16.melting_point, "melting_point")
load_data_from_dict(group_16.boiling_point, "boiling_point")

load_data_from_dict(group_17.electronegativity, "electronegativity")
load_data_from_dict(group_17.atomic_radii, "atomic_radius")
load_data_from_dict(group_17.density, "density")
load_data_from_dict(group_17.melting_point, "melting_point")
load_data_from_dict(group_17.boiling_point, "boiling_point")

load_data_from_dict(group_18.electronegativity, "electronegativity")
load_data_from_dict(group_18.atomic_radii, "atomic_radius")
load_data_from_dict(group_18.density, "density")
load_data_from_dict(group_18.melting_point, "melting_point")
load_data_from_dict(group_18.boiling_point, "boiling_point")



# Add all other groups similarly...

# Blocks

load_data_from_dict(s_block.electronegativity, "electronegativity")
load_data_from_dict(s_block.atomic_radii, "atomic_radius")
load_data_from_dict(s_block.density, "density")
load_data_from_dict(s_block.melting_point, "melting_point")
load_data_from_dict(s_block.boiling_point, "boiling_point")

load_data_from_dict(p_block.electronegativity, "electronegativity")
load_data_from_dict(p_block.atomic_radii, "atomic_radius")
load_data_from_dict(p_block.density, "density")
load_data_from_dict(p_block.melting_point, "melting_point")
load_data_from_dict(p_block.boiling_point, "boiling_point")

load_data_from_dict(d_block.electronegativity, "electronegativity")
load_data_from_dict(d_block.atomic_radii, "atomic_radius")
load_data_from_dict(d_block.density, "density")
load_data_from_dict(d_block.melting_point, "melting_point")
load_data_from_dict(d_block.boiling_point, "boiling_point")

load_data_from_dict(f_block.electronegativity, "electronegativity")
load_data_from_dict(f_block.atomic_radii, "atomic_radius")
load_data_from_dict(f_block.density, "density")
load_data_from_dict(f_block.melting_point, "melting_point")
load_data_from_dict(f_block.boiling_point, "boiling_point")
# ... etc


# ============================================================
# Group membership (for trend analysis)
# ============================================================

GROUP_MEMBERSHIP = {
    "H": 1, "Li": 1, "Na": 1, "K": 1, "Rb": 1, "Cs": 1, "Fr": 1,
    "Be": 2, "Mg": 2, "Ca": 2, "Sr": 2, "Ba": 2, "Ra": 2,
    "Be": 2, "Mg": 2, "Ca": 2, "Sr": 2,
    "Sc": 3, "Y": 3, "La": 3, "Ac": 3,
    "Ti": 4, "Zr": 4, "Hf": 4, "Rf": 4,
    "V": 5, "Nb": 5, "Ta": 5, "Db": 5,
    "Cr": 6, "Mo": 6, "W": 6, "Sg": 6,
    "Mn": 7, "Tc": 7, "Re": 7, "Bh": 7,
    "Fe": 8, "Ru": 8, "Os": 8, "Hs": 8,
    "Co": 9, "Rh": 9, "Ir": 9, "Mt": 9,
    "Ni": 10, "Pd": 10, "Pt": 10, "Ds": 10,
    "Cu": 11, "Ag": 11, "Au":  11, "Rg": 11,
    "Zn": 12, "Cd": 12, "Hg": 12, "Cn": 12,
    "B": 13, "Al": 13, "Ga": 13, "In": 13, "Tl": 13, "Nh": 13,
    "C": 14, "Si": 14, "Ge": 14, "Sn": 14, "Pb": 14, "Fl": 14,
    "N": 15, "P": 15, "As": 15, "Sb": 15, "Bi": 15, "Mc": 15,
    "O": 16, "S": 16, "Se": 16, "Te": 16, "Po": 16, "Lv": 16,
    "F": 17, "Cl": 17, "Br": 17, "I": 17, "At": 17, "Ts": 17,
    "He": 18, "Ne": 18, "Ar": 18, "Kr": 18, "Xe": 18, "Rn": 18, "Og": 18,
}


PERIOD_MEMBERSHIP = {
    "H": 1, "He": 1,
    "Li": 2, "Be": 2, "B": 2, "C": 2, "N": 2, "O": 2, "F": 2, "Ne": 2,
    "Na": 3, "Mg": 3, "Al": 3, "Si": 3, "P": 3, "S": 3, "Cl": 3, "Ar": 3,
    "K": 4, "Ca": 4, "Sc": 4, "Ti": 4, "V": 4, "Cr": 4, "Mn": 4, "Fe": 4, "Co": 4, "Ni": 4, "Zn": 4, "Cu": 4, "Ga": 4, "As": 4, "Se": 4, "Br": 4, "Kr": 4, "Ge": 4,
    "Rb": 5, "Sr": 5, "Y": 5, "Zr": 5, "Nb": 5, "Mo": 5, "Tc": 5, "Rh": 5, "Ru": 5, "Pd": 5, "Ag": 5, "Cd": 5, "In": 5, "Sn": 5, "Sb": 5, "Te": 5, "I": 5, "Xe": 5,
    "Cs": 6, "Ba": 6, "La": 6, "Hf": 6, "Ta": 6, "Re": 6, "W": 6, "Os": 6, "Ir": 6, "Pt": 6, "Au": 6, "Hg": 6, "Tl": 6, "Pb": 6, "Bi": 6, "Po": 6, "At": 6, "Rn": 6,
    "Fr": 7, "Ra": 7, "Ac": 7, "Rf": 7, "Db": 7, "Bh": 7, "Sg": 7, "Hs": 7, "Mt": 7, "Ds": 7, "Rg": 7, "Cn": 7, "Nh": 7, "Fl": 7, "Mc": 7, "Lv": 7, "Ts": 7, "Og": 7,
}


# ============================================================
# Access functions
# ============================================================

def get_element_data(symbol: str) -> Optional[Dict]:
    """Get all data for an element"""
    return ELEMENT_DATA.get(symbol)


def get_property(symbol: str, property_name: str):
    """Get a specific property of an element"""
    return ELEMENT_DATA.get(symbol, {}).get(property_name)


def get_group_elements(group: int) -> list:
    """Get all elements in a group"""
    return [e for e, g in GROUP_MEMBERSHIP.items() if g == group]


def get_period_elements(period: int) -> list:
    """Get all elements in a period"""
    return [e for e, p in PERIOD_MEMBERSHIP.items() if p == period]


# ============================================================
# Property name mapping (what user says → internal key)
# ============================================================

PROPERTY_ALIASES = {
    "electronegativity": "electronegativity",
    "en": "electronegativity",
    "atomic radius": "atomic_radius",
    "atomic radii": "atomic_radius",
    "radius": "atomic_radius",
    "density": "density",
    "melting point": "melting_point",
    "mp": "melting_point",
    "boiling point": "boiling_point",
    "bp": "boiling_point",
}


def resolve_property(user_input: str) -> Optional[str]:
    """Convert user input to internal property name"""
    user_input = user_input.lower().strip()
    for alias, prop in PROPERTY_ALIASES.items():
        if alias in user_input or user_input == alias:
            return prop
    return None