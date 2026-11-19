"""Phenomenological Lorentzian bath response and detailed balance.
NOT a calibrated magnon spectrum or a derivation of coupling from geometry.
"""
import math
from phase2_nv_screen import equilibrium_excited_fraction

def lorentzian_spectral_density(probe_hz,center_hz,linewidth_hz,peak_rate):
    if min(probe_hz,center_hz,peak_rate)<0 or linewidth_hz<=0:
        raise ValueError("invalid spectral parameter")
    return peak_rate/(1+(2*(probe_hz-center_hz)/linewidth_hz)**2)

def detailed_balance_rates(transition_hz,temperature_k,total_rate):
    if transition_hz<=0 or temperature_k<=0 or total_rate<0:
        raise ValueError("invalid bath parameters")
    p=equilibrium_excited_fraction(temperature_k,transition_hz)
    return total_rate*p,total_rate*(1-p)

def spectral_rates(transition_hz,temp_k,center_hz,linewidth_hz,peak_rate):
    rate=lorentzian_spectral_density(transition_hz,center_hz,linewidth_hz,peak_rate)
    return detailed_balance_rates(transition_hz,temp_k,rate)

if __name__=="__main__":
    for t in (300,600):
        for center in (2.87e9,3.0e9):
            up,down=spectral_rates(2.87e9,t,center,20e6,1e5)
            print(f"T={t}K center={center/1e9:.3f}GHz up={up:.4f}/s down={down:.4f}/s")
    print("Rates depend on assumed peak and linewidth, not measured magnetic-film data.")
