# modules/chemistry/router.py

"""
Chemistry Module Router
Routes chemistry questions to appropriate sub-modules:
- Physical Chemistry (mole concept, stoichiometry, thermo, equilibrium)
- Inorganic Chemistry (periodic trends, coordination compounds)
- Organic Chemistry (reactions, functional groups)
"""

import re
from physical import mole_concept, stoichiometry
from inorganic import periodic_trends

class ChemistryRouter:
    def __init__(self):
        self.routes = {
            # Physical Chemistry
            "mole_concept": {
                "keywords": ["mole", "molarity", "molality", "w/v", "w/w", "v/v", "density", "concentration", "mass", "volume"],
                "module": mole_concept
            },
            "stoichiometry": {
                "keywords": ["balance", "limiting reagent", "yield", "stoichiometry", "reactant", "product"],
                "module": stoichiometry
            },
            "thermo": {
                "keywords": ["enthalpy", "entropy", "gibbs", "ΔH", "ΔS", "ΔG", "heat", "thermochemistry"],
                "module": None  # TODO: Add thermo module
            },
            "equilibrium": {
                "keywords": ["equilibrium", "kc", "kp", "ice table", "le chatelier"],
                "module": None  # TODO: Add equilibrium module
            },
            
            # Inorganic Chemistry
            "periodic_trends": {
                "keywords": ["electronegativity", "atomic radius", "ionization energy", "trend", "periodic", "group", "period"],
                "module": periodic_trends
            },
            "coordination": {
                "keywords": ["coordination", "ligand", "complex", "oxidation state", "cfse"],
                "module": None  # TODO: Add coordination module
            },
            
            # Organic Chemistry
            # "reactions": {
            #     "keywords": ["reaction", "named reaction", "mechanism", "synthesis", "product"],
            #     "module": reactions
            # },
            "functional_groups": {
                "keywords": ["functional group", "alcohol", "aldehyde", "ketone", "carboxylic", "amine"],
                "module": None  # TODO: Add functional groups module
            },
        }