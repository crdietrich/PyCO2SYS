# PyCO2SYS: marine carbonate system calculations in Python.
# Copyright (C) 2020  Matthew Paul Humphreys et al.  (GNU GPLv3)
"Calculate various buffer factors of the marine carbonate system."

from . import solve

def buffers_ESM10(TC, TA, CO2, HCO3, CO3, pH, OH, BAlk, KB):
    """Buffer factors from ESM10 with corrections for typographical errors
    described in the supp. info. to RAH18.
    """
    H = 10.0**-pH
    # Evaluate ESM10 subfunctions (from their Table 1)
    S = HCO3 + 4*CO3 + H*BAlk/(KB + H) + H + OH # -OH => +OH in v1.2.1
    # Typo in ESM10 carried through here, spotted by Jim Orr, following OEDG18
    P = 2*CO2 + HCO3
    Q = HCO3 - H*BAlk/(KB + H) - H - OH # see RAH18
    AC = HCO3 + 2*CO3
    # Calculate buffer factors
    gammaTC = TC - AC**2/S
    betaTC = (TC*S - AC**2)/AC
    omegaTC = TC - AC*P/Q # corrected, see RAH18 supp. info.
    ## omegaTC = TC - AC*P/HCO3 # original ESM10 equation, WRONG
    gammaTA = (AC**2 - TC*S)/AC
    betaTA = AC**2/TC - S
    omegaTA = AC - TC*Q/P # corrected as for omegaTC (RAH18), HCO3 => Q
    ## omegaTA = AC - TC*HCO3/P # original ESM10 equation, WRONG
    return gammaTC, betaTC, omegaTC, gammaTA, betaTA, omegaTA

def bgc_isocap(CO2, pH, K1, K2, KB, KW, TB):
    """Isocapnic quotient of HDW18, Eq. 8."""
    h = 10.0**-pH
    return ((K1*CO2*h + 4*K1*K2*CO2 + KW*h + h**3)*(KB + h)**2 +
        KB*TB*h**3)/(K1*CO2*(2*K2 + h)*(KB + h)**2)

def bgc_isocap_approx(TC, pCO2, K0, K1, K2):
    """Approximate isocapnic quotient of HDW18, Eq. 7."""
    return 1 + 2*(K2/(K0*K1))*TC/pCO2

def psi(CO2, pH, K1, K2, KB, KW, TB):
    """Psi of FCG94."""
    Q = bgc_isocap(CO2, pH, K1, K2, KB, KW, TB)
    return -1 + 2/Q

def RevelleFactor(TA, TC, K0,
        K1, K2, KW, KB, KF, KS, KP1, KP2, KP3, KSi, KNH3, KH2S,
        TB, TF, TSO4, TPO4, TSi, TNH3, TH2S):
    """Calculate the Revelle Factor from total alkalinity and dissolved
    inorganic carbon.

    This calculates the Revelle factor (dfCO2/dTC)|TA/(fCO2/TC).
    It only makes sense to talk about it at pTot = 1 atm, but it is computed
    here at the given K(), which may be at pressure <> 1 atm. Care must
    thus be used to see if there is any validity to the number computed.

    Based on RevelleFactor, version 01.03, 01-07-97, by Ernie Lewis.
    """
    Ts = [TB, TF, TSO4, TPO4, TSi, TNH3, TH2S]
    Ks = [K1, K2, KW, KB, KF, KS, KP1, KP2, KP3, KSi, KNH3, KH2S]
    dTC = 1e-6 # 1 umol/kg-SW
    # Find fCO2 at TA, TC+dTC
    TC_plus = TC + dTC
    pH_plus = solve.pHfromTATC(TA, TC_plus, *Ks, *Ts)
    fCO2_plus = solve.fCO2fromTCpH(TC_plus, pH_plus, K0, K1, K2)
    # Find fCO2 at TA, TC-dTC
    TC_minus = TC - dTC
    pH_minus = solve.pHfromTATC(TA, TC_minus, *Ks, *Ts)
    fCO2_minus = solve.fCO2fromTCpH(TC_minus, pH_minus, K0, K1, K2)
    # Calculate Revelle Factor
    Revelle = ((fCO2_plus - fCO2_minus)/dTC /
               ((fCO2_plus + fCO2_minus)/TC_minus))
    return Revelle
