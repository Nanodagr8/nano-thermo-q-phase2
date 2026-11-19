"""Phase 2 equal-resource detuning/decoherence screening. No experimental claims."""
import numpy as np
from scipy.linalg import expm
from phase2_nv_screen import equilibrium_excited_fraction
SX=np.array([[0,1],[1,0]],complex)
SZ=np.diag([1,-1]).astype(complex)
DOWN=np.array([[0,1],[0,0]],complex)
UP=DOWN.conj().T

def channel(temperature_k, rabi_hz, detuning_hz, pulse_s, t1_s, tphi_s, pump_hz=0.):
    if min(rabi_hz,pulse_s,pump_hz)>=0 and t1_s>0 and tphi_s>0:
        pass
    else: raise ValueError("invalid rates or duration")
    pe=equilibrium_excited_fraction(temperature_k)
    jumps=((DOWN,(1-pe)/t1_s+pump_hz),(UP,pe/t1_s),(SZ,1/(2*tphi_s)))
    h=np.pi*(rabi_hz*SX+detuning_hz*SZ)
    def rhs(rho):
        y=-1j*(h@rho-rho@h)
        for l,rate in jumps:
            g=l.conj().T@l
            y+=rate*(l@rho@l.conj().T-0.5*(g@rho+rho@g))
        return y
    basis=[]
    for i in range(2):
        for j in range(2):
            b=np.zeros((2,2),complex);b[i,j]=1
            basis.append(b)
    generator=np.column_stack([rhs(b).reshape(4) for b in basis])
    return expm(generator*pulse_s)

def apply(superoperator,rho):
    return (superoperator@rho.reshape(4)).reshape((2,2))

def average_gate_fidelity_to_x(superoperator):
    """Exact six cardinal pure-state average; equals qubit average gate fidelity."""
    plus=np.array([1,1],complex)/np.sqrt(2)
    minus=np.array([1,-1],complex)/np.sqrt(2)
    plus_i=np.array([1,1j],complex)/np.sqrt(2)
    minus_i=np.array([1,-1j],complex)/np.sqrt(2)
    states=(np.array([1,0],complex),np.array([0,1],complex),plus,minus,plus_i,minus_i)
    vals=[]
    for psi in states:
        rho=np.outer(psi,psi.conj())
        target=SX@rho@SX
        vals.append(float(np.trace(target@apply(superoperator,rho)).real))
    return float(np.mean(vals))

def sweep():
    rabi=1e6
    duration=0.5/rabi
    for t,t1,tphi in ((300,1e-3,1e-3),(600,0.2e-3,0.2e-3)):
        for detuning in (0,0.1e6,0.5e6):
            f=average_gate_fidelity_to_x(channel(t,rabi,detuning,duration,t1,tphi))
            yield (t,t1,tphi,detuning,f)
if __name__=="__main__":
    print("ASSUMED temperature-dependent T1/Tphi; equal drive and pulse duration; no measured material parameters")
    for x in sweep(): print("T_K=%g T1_s=%g Tphi_s=%g detuning_Hz=%g avg_X_gate_fidelity=%.9f"%x)
