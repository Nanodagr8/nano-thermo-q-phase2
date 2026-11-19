"""Phase 2 thermal magnon noise: distinguish stochastic fluctuations from coherent drive.
Ornstein-Uhlenbeck frequency noise is phenomenological, NOT material-calibrated.
"""
import numpy as np
from phase2_nv_gate_screen import SX,SZ
from scipy.linalg import expm

def simulate_noise(temp_k, shots=1000, steps=60, seed=20261118,
                   base_noise_hz=1e5, correlation_s=0.1e-6,
                   pulse_s=0.5e-6, rabi_hz=1e6):
    if temp_k<=0 or shots<=0 or steps<=0 or correlation_s<=0 or pulse_s<0 or min(base_noise_hz,rabi_hz)<0:
        raise ValueError("invalid parameters")
    rng=np.random.default_rng(seed)
    dt=pulse_s/steps
    a=np.exp(-dt/correlation_s)
    std=base_noise_hz*np.sqrt(temp_k/300.)
    noise=rng.normal(0,std,shots)
    states=np.zeros((shots,2),complex); states[:,0]=1
    for _ in range(steps):
        noise=a*noise+np.sqrt(1-a*a)*rng.normal(0,std,shots)
        # H/hbar = pi*(rabi*sigma_x + noise*sigma_z).
        omega=np.sqrt(rabi_hz*rabi_hz+noise*noise)
        angle=np.pi*omega*dt
        c=np.cos(angle);s=np.sin(angle)
        x=states[:,0].copy();y=states[:,1].copy()
        scale=np.divide(s,omega,out=np.full_like(omega,np.pi*dt),where=omega>0)
        states[:,0]=c*x-1j*scale*(noise*x+rabi_hz*y)
        states[:,1]=c*y-1j*scale*(rabi_hz*x-noise*y)
    return {"temperature_k":temp_k,"shots":shots,"seed":seed,
            "mean_excited":float(np.mean(abs(states[:,1])**2)),
            "mean_norm":float(np.mean(np.sum(abs(states)**2,axis=1))),
            "noise_std_hz":std}

def thermal_null_control(temp_k,shots=1000,seed=20261118):
    return simulate_noise(temp_k,shots=shots,seed=seed,rabi_hz=0.)

if __name__=="__main__":
    for temp in (300,600):
        print("driven",simulate_noise(temp))
        print("thermal_noise_only",thermal_null_control(temp))
    print("Noise-only diagonal sigma_z cannot flip an initial sigma_z eigenstate; stochastic noise is not a coherent drive.")
