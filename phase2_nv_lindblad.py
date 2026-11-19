"""Phase 2 open-system NV toy model. Assumed rates, not measured device parameters."""
import numpy as np
from scipy.linalg import expm
from phase2_nv_screen import equilibrium_excited_fraction

SM=np.array([[0,1],[0,0]],complex)
SP=SM.conj().T
SZ=np.diag([1.,-1.]).astype(complex)
SX=SM+SP

def lindblad_rhs(rho, hamiltonian, jumps):
    drho=-1j*(hamiltonian@rho-rho@hamiltonian)
    for operator,rate in jumps:
        if rate < 0: raise ValueError("rates must be nonnegative")
        dagger=operator.conj().T
        gram=dagger@operator
        drho+=rate*(operator@rho@dagger-0.5*(gram@rho+rho@gram))
    return drho

def evolve(temp_k, duration_s, rabi_hz=0., t1_s=1e-3, tphi_s=1e-3,
           optical_pump_hz=0., initial_excited=0.5):
    """Two-level rotating-frame model; optical pumping is phenomenological."""
    if duration_s<0 or rabi_hz<0 or t1_s<=0 or tphi_s<=0 or optical_pump_hz<0:
        raise ValueError("invalid physical parameter")
    if not 0<=initial_excited<=1: raise ValueError("invalid population")
    p=equilibrium_excited_fraction(temp_k)
    jumps=[(SM,(1-p)/t1_s+optical_pump_hz),(SP,p/t1_s),
           (SZ,1/(2*tphi_s))]
    hamiltonian=np.pi*rabi_hz*SX
    basis=[np.eye(2,dtype=complex)[:,i:i+1]@np.eye(2,dtype=complex)[j:j+1,:] for i in range(2) for j in range(2)]
    generator=np.column_stack([lindblad_rhs(b,hamiltonian,jumps).reshape(4) for b in basis])
    rho0=np.diag([1-initial_excited,initial_excited]).astype(complex)
    coefficients=np.array([rho0[i,j] for i in range(2) for j in range(2)])
    rho=(expm(generator*duration_s)@coefficients).reshape((2,2))
    return rho

def summarize(rho):
    return {"excited_population":float(rho[1,1].real),
            "trace":float(np.trace(rho).real),
            "minimum_eigenvalue":float(np.linalg.eigvalsh((rho+rho.conj().T)/2).min())}

if __name__=="__main__":
    for t in (300.,600.):
        for pump in (0.,1e5):
            result=summarize(evolve(t,0.005,optical_pump_hz=pump))
            print(f"T={t:g} K pump={pump:g}/s {result}")
    print("ASSUMED rates; illustrative open-system simulation, not a gate-fidelity measurement.")
