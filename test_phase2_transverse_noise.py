import unittest
import numpy as np
from phase2_transverse_noise import thermal_channel,sensitivity
from phase2_nv_gate_screen import apply,average_gate_fidelity_to_x
class TestTransverse(unittest.TestCase):
    def test_positive_trace(self):
        for t,rate,_,_ in sensitivity():
            rho=apply(thermal_channel(t,extra_transverse_rate_hz=rate),np.diag([1.,0.]))
            self.assertAlmostEqual(np.trace(rho).real,1.,places=9)
            self.assertGreaterEqual(np.linalg.eigvalsh((rho+rho.conj().T)/2).min(),-1e-10)
    def test_extra_noise_degrades_gate(self):
        a=average_gate_fidelity_to_x(thermal_channel(300,extra_transverse_rate_hz=0))
        b=average_gate_fidelity_to_x(thermal_channel(300,extra_transverse_rate_hz=1e6))
        self.assertGreater(a,b)
    def test_transverse_noise_can_flip(self):
        a=apply(thermal_channel(300,drive_hz=0,extra_transverse_rate_hz=1e6),np.diag([1.,0.]))[1,1].real
        b=apply(thermal_channel(300,drive_hz=0,extra_transverse_rate_hz=0),np.diag([1.,0.]))[1,1].real
        self.assertGreater(a,b)
    def test_ideal_pi(self):
        self.assertAlmostEqual(average_gate_fidelity_to_x(thermal_channel(300,t1_s=1e12,tphi_s=1e12)),1.,places=8)
    def test_invalid(self):
        with self.assertRaises(ValueError): thermal_channel(300,extra_transverse_rate_hz=-1)
if __name__=="__main__": unittest.main()
