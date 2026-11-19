"""Phenomenological transverse thermal noise: rates not measured or FDT-calibrated."""
import numpy as np
from scipy.linalg import expm
from phase2_nv_gate_screen import SX,SZ,DOWN,UP,apply,average_gate_fidelity_to_x

def thermal_channel(temp_k,drive_hz=1e6,duration_s=0.5e-6,
                    t1_s=1e-3,tphi_s=1e-3,extra_transverse_rate_hz=0.):
    if temp_k<=0 or drive_hz<0 or duration_s<0 or t1_s<=0 or tphi_s<=0 or extra_transverse_rate_hz<0:
        raise ValueError("invalid physical input")
    from phase2_nv_screen import equilibrium_excited_fraction
    p=equilibrium_excited_fraction(temp_k)
    h=np.pi*drive_hz*SX
    # Symmetric extra up/down noise: infinite-temperature transverse bath surrogate.
    jumps=((DOWN,(1-p)/t1_s+extra_transverse_rate_hz),
           (UP,p/t1_s+extra_transverse_rate_hz),
           (SZ,1/(2*tphi_s)))
    def derivative(rho):
        out=-1j*(h@rho-rho@h)
        for op,rate in jumps:
            gram=op.conj().T@op
            out+=rate*(op@rho@op.conj().T-(gram@rho+rho@gram)/2)
        return out
    basis=[]
    for i in range(2):
        for j in range(2):
            b=np.zeros((2,2),complex);b[i,j]=1;basis.append(b)
    generator=np.column_stack([derivative(b).reshape(4) for b in basis])
    return expm(generator*duration_s)

def sensitivity():
    for temp in (300.,600.):
        for rate in (0.,1e4,1e5,1e6):
            ch=thermal_channel(temp,extra_transverse_rate_hz=rate)
            yield temp,rate,average_gate_fidelity_to_x(ch),float(apply(ch,np.diag([1.,0.]))[1,1].real)
if __name__=="__main__":
    for row in sensitivity():
        print("T_K=%g transverse_rate_per_s=%g avg_X_fidelity=%.9f excited_from_ground=%.9f"%row)
    print("Rate is an independent assumed variable; temperature does not determine it in this screen.")
