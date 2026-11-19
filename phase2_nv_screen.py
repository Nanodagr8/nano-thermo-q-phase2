"""Phase 2 analytic NV control screening; NOT a thermal quantum hardware model."""
import math
KB=1.380649e-23
H=6.62607015e-34
NV_HZ=2.87e9

def equilibrium_excited_fraction(temp_k, splitting_hz=NV_HZ):
    if temp_k <= 0 or splitting_hz <= 0:
        raise ValueError("positive temperature and splitting required")
    x=H*splitting_hz/(KB*temp_k)
    return 1.0/(1.0+math.exp(x))

def resonant_rotation(rabi_hz, duration_s):
    if rabi_hz < 0 or duration_s < 0:
        raise ValueError("nonnegative drive and time required")
    theta=2*math.pi*rabi_hz*duration_s
    return math.sin(theta/2)**2

def screening_table():
    return [(t,equilibrium_excited_fraction(t),1-2*equilibrium_excited_fraction(t)) for t in (300.,450.,600.)]

if __name__=="__main__":
    for t,p,pol in screening_table():
        print(f"T={t:g} K; excited_fraction={p:.10f}; thermal_polarization={pol:.10f}")
    print("All quantities are analytic idealizations; no heat-to-B1 or gate fidelity claim.")
