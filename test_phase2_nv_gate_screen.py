import unittest
import numpy as np
from phase2_nv_gate_screen import channel,apply,average_gate_fidelity_to_x,sweep
class TestGateScreen(unittest.TestCase):
    def test_ideal_pi_x(self):
        s=channel(300,1e6,0,0.5e-6,1e12,1e12)
        self.assertAlmostEqual(average_gate_fidelity_to_x(s),1.,places=8)
    def test_detuning_penalty(self):
        a=average_gate_fidelity_to_x(channel(300,1e6,0,0.5e-6,1e-3,1e-3))
        b=average_gate_fidelity_to_x(channel(300,1e6,0.5e6,0.5e-6,1e-3,1e-3))
        self.assertGreater(a,b)
    def test_decoherence_penalty(self):
        a=average_gate_fidelity_to_x(channel(300,1e6,0,0.5e-6,1e-3,1e-3))
        b=average_gate_fidelity_to_x(channel(600,1e6,0,0.5e-6,0.2e-3,0.2e-3))
        self.assertGreater(a,b)
    def test_trace_and_positivity(self):
        for row in sweep():
            t,t1,tphi,detuning,_=row
            s=channel(t,1e6,detuning,0.5e-6,t1,tphi)
            rho=apply(s,np.array([[1,0],[0,0]],complex))
            self.assertAlmostEqual(np.trace(rho).real,1,places=9)
            self.assertGreaterEqual(np.linalg.eigvalsh((rho+rho.conj().T)/2).min(),-1e-10)
    def test_invalid(self):
        with self.assertRaises(ValueError): channel(300,-1,0,1e-6,1e-3,1e-3)
if __name__=="__main__": unittest.main()
