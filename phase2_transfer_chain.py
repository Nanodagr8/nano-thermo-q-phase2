"""Phase 2 dimensional transfer-chain screen, NOT a calibrated heat-to-qubit model.
A deliberately parameterized linear-response hypothesis with a null coupling control.
"""
import math
import numpy as np
KB=1.380649e-23
HBAR=1.054571817e-34
GAMMA_E=1.76085963023e11  # rad s^-1 T^-1, free electron magnitude

def bose_occupation(freq_hz,temp_k):
    if freq_hz<=0 or temp_k<=0: raise ValueError("positive frequency and temperature required")
    x=2*math.pi*HBAR*freq_hz/(KB*temp_k)
    return 1/math.expm1(x)

def thermal_magnon_to_b1(freq_hz, cold_k, hot_k, coupling_t_per_sqrt_magnon, efficiency=1.):
    """Hypothesis: B1 = g sqrt(eta delta_n); g is T/sqrt(magnon), not experimentally determined."""
    if hot_k<cold_k or coupling_t_per_sqrt_magnon<0 or not 0<=efficiency<=1:
        raise ValueError("invalid heating or coupling")
    delta=max(0.,bose_occupation(freq_hz,hot_k)-bose_occupation(freq_hz,cold_k))
    return coupling_t_per_sqrt_magnon*math.sqrt(efficiency*delta)

def rabi_hz_from_b1(b1_t):
    if b1_t<0: raise ValueError("negative field")
    return GAMMA_E*b1_t/(2*math.pi)

def screen(samples=10000,seed=42):
    """Independent loguniform assumed g [1e-12,1e-8] T/sqrt(magnon), eta [0,1].
    Assumptions are wide, arbitrary sensitivity bounds; NOT material uncertainty intervals."""
    if samples<=0: raise ValueError("samples must be positive")
    rng=np.random.default_rng(seed)
    coupling=10**rng.uniform(-12,-8,samples)
    eta=rng.uniform(0,1,samples)
    cold,hot,freq=300.,600.,2.87e9
    occupancy_change=bose_occupation(freq,hot)-bose_occupation(freq,cold)
    b1=coupling*np.sqrt(eta*occupancy_change)
    rabi=GAMMA_E*b1/(2*np.pi)
    return {"occupancy_change":float(occupancy_change),
            "B1_T_quantiles":np.quantile(b1,[.05,.5,.95]).tolist(),
            "Rabi_Hz_quantiles":np.quantile(rabi,[.05,.5,.95]).tolist(),
            "null_B1_T":thermal_magnon_to_b1(freq,cold,hot,0.),
            "seed":seed,"samples":samples}

if __name__=="__main__":
    print(screen())
    print("Sensitivity only. Thermal magnons are not assumed phase-coherent; B1 is a hypothetical coherent-equivalent field, not an experimentally supported prediction.")
