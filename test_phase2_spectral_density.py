import unittest
from phase2_spectral_density import lorentzian_spectral_density, detailed_balance_rates
class TestSpectralDensity(unittest.TestCase):
 def test_peak(self):
  self.assertGreater(lorentzian_spectral_density(2.87e9,2.87e9,1e7,1),lorentzian_spectral_density(3e9,2.87e9,1e7,1))
 def test_nonnegative(self):
  self.assertGreaterEqual(lorentzian_spectral_density(2.87e9,2.87e9,1e7,0),0)
 def test_balance(self):
  up,down=detailed_balance_rates(2.87e9,300,1000)
  from phase2_nv_screen import equilibrium_excited_fraction
  self.assertAlmostEqual(up/(up+down),equilibrium_excited_fraction(300),places=12)
 def test_temperature(self):
  a=detailed_balance_rates(2.87e9,300,1000)
  b=detailed_balance_rates(2.87e9,600,1000)
  self.assertGreater(b[0]/b[1],a[0]/a[1])
 def test_invalid(self):
  with self.assertRaises(ValueError): detailed_balance_rates(2.87e9,0,1000)
  with self.assertRaises(ValueError): lorentzian_spectral_density(2.87e9,2.87e9,0,1)
if __name__=="__main__":unittest.main()
