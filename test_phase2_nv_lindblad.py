import unittest
import numpy as np
from phase2_nv_lindblad import evolve,summarize
from phase2_nv_screen import equilibrium_excited_fraction
class TestNVLindblad(unittest.TestCase):
    def test_trace_positive(self):
        for t in (300.,600.):
            for pump in (0.,1e5):
                x=summarize(evolve(t,0.005,optical_pump_hz=pump))
                self.assertAlmostEqual(x["trace"],1,places=10)
                self.assertGreater(x["minimum_eigenvalue"],-1e-10)
    def test_thermal_equilibrium(self):
        for t in (300.,600.):
            self.assertAlmostEqual(summarize(evolve(t,0.02))["excited_population"],equilibrium_excited_fraction(t),places=7)
    def test_pump_reduces_excitation(self):
        self.assertLess(summarize(evolve(600,0.005,optical_pump_hz=1e5))["excited_population"],summarize(evolve(600,0.005))["excited_population"])
    def test_unitary_pi(self):
        rho=evolve(300,0.5e-6,rabi_hz=1e6,t1_s=1e12,tphi_s=1e12,initial_excited=0)
        self.assertAlmostEqual(rho[1,1].real,1.,places=7)
    def test_invalid(self):
        with self.assertRaises(ValueError): evolve(300,-1)
    def test_zero_duration(self):
        self.assertAlmostEqual(evolve(300,0,initial_excited=.2)[1,1].real,.2)
if __name__=="__main__": unittest.main()
