import unittest
from phase2_nv_screen import equilibrium_excited_fraction, resonant_rotation, screening_table
class TestNVScreen(unittest.TestCase):
    def test_thermal_near_half(self):
        self.assertTrue(0.49 < equilibrium_excited_fraction(300) < 0.5)
    def test_heating_reduces_polarization(self):
        self.assertGreater(1-2*equilibrium_excited_fraction(300),1-2*equilibrium_excited_fraction(600))
    def test_monotonic(self):
        self.assertEqual([x[0] for x in screening_table()],[300.,450.,600.])
    def test_pi_pulse(self):
        self.assertAlmostEqual(resonant_rotation(1e6,0.5e-6),1.)
    def test_zero_drive(self):
        self.assertEqual(resonant_rotation(0,1),0)
    def test_invalid_temperature(self):
        with self.assertRaises(ValueError): equilibrium_excited_fraction(0)
if __name__=="__main__": unittest.main()
