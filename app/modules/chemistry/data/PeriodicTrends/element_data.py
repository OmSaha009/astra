# chemistry/data/element_data.py

"""
Unified access layer for all element data.
Import from block and group files and provide a single interface.
"""

# Import all your existing data
from app.modules.chemistry.data.PeriodicTrends.Blocks.s_block import S_BLOCK_DATA
from app.modules.chemistry.data.PeriodicTrends.Blocks.p_block import P_BLOCK_DATA
from app.modules.chemistry.data.PeriodicTrends.Blocks.d_block import D_BLOCK_DATA
from app.modules.chemistry.data.PeriodicTrends.Blocks.f_block import F_BLOCK_DATA

# Combine into one master dictionary
ELEMENT_DATA = {}

# Add elements from all sources
for element, props in S_BLOCK_DATA.items():
    ELEMENT_DATA[element] = props

for element, props in P_BLOCK_DATA.items():
    ELEMENT_DATA[element] = props

# ... add all others

# Also store group membership
GROUP_MEMBERSHIP = {
    "Li": 1, "Na": 1, "K": 1, "Rb": 1, "Cs": 1, "Fr": 1,
    "Be": 2, "Mg": 2, "Ca": 2, "Sr": 2, "Ba": 2, "Ra": 2,
    "F": 17, "Cl": 17, "Br": 17, "I": 17, "At": 17,
    # ... add all
}

PERIOD_MEMBERSHIP = {
    "H": 1, "He": 1,
    "Li": 2, "Be": 2, "B": 2, "C": 2, "N": 2, "O": 2, "F": 2, "Ne": 2,
    "Na": 3, "Mg": 3, "Al": 3, "Si": 3, "P": 3, "S": 3, "Cl": 3, "Ar": 3,
    # ... add all
}


def get_element_data(element: str) -> dict:
    """Get all properties for an element"""
    return ELEMENT_DATA.get(element, {})


def get_property(element: str, property_name: str):
    """Get specific property of an element"""
    return ELEMENT_DATA.get(element, {}).get(property_name)


def get_group_elements(group: int) -> list:
    """Get all elements in a group"""
    return [e for e, g in GROUP_MEMBERSHIP.items() if g == group]


def get_period_elements(period: int) -> list:
    """Get all elements in a period"""
    return [e for e, p in PERIOD_MEMBERSHIP.items() if p == period]