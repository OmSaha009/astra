from ..physical.mole_concept import atomic_mass, calculate_molar_mass 

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

def mass_to_moles(mass, molar_mass):
    return round( mass/molar_mass ,3)

def moles_to_mass(moles, molar_mass):
    return round(moles * molar_mass, 3)


def molarity_to_moles(M, volume):
    return round(M * volume, 3)


def moles_to_molarity(moles, volume):
    return round(moles / volume, 3)

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

def ppm_to_molarity(ppm, molar_mass, density=1):
    """ppm to Molarity (assuming dilute aqueous)"""
    return round((ppm / molar_mass) / 1000, 6)

def molarity_to_ppm(M, molar_mass):
    """Molarity to ppm"""
    return round(M * molar_mass * 1000, 2)


def ppm_element_to_compound_mass(ppm, solution_mass, element, compound):
    
    # 1. element mass in grams
    element_mass = (ppm / 1e6) * solution_mass

    # 2. molar masses
    element_mm = atomic_mass(element)
    compound_mm = calculate_molar_mass(compound)

    # 3. scale up
    compound_mass = element_mass * (compound_mm / element_mm)

    return compound_mass