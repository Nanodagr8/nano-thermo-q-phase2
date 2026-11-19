import unittest
from phase2_transfer_chain import bose_occupation,thermal_magnon_to_b1,rabi_hz_from_b1,screen
class TestTransfer(unittest.TestCase):
    def test_bose_temperature(self):
        self.assertGreater(bose_occupation(2.87e9,600),bose_occupation(2.87e9,300))
    def test_null_coupling(self):
        self.assertEqual(thermal_magnon_to_b1(2.87e9,300,600,0),0)
    def test_zero_heating(self):
        self.assertEqual(thermal_magnon_to_b1(2.87e9,300,300,1e-9),0)
    def test_efficiency(self):
        self.assertEqual(thermal_magnon_to_b1(2.87e9,300,600,1e-9,0),0)
    def test_monotone_coupling(self):
        self.assertAlmostEqual(thermal_magnon_to_b1(2.87e9,300,600,2e-9),2*thermal_magnon_to_b1(2.87e9,300,600,1e-9))
    def test_rabi_conversion(self):
        self.assertGreater(rabi_hz_from_b1(1e-6),0)
    def test_reproducibility(self):
        self.assertEqual(screen(500,7),screen(500,7))
    def test_quantile_order(self):
        x=screen(1000)
        self.assertEqual(x["null_B1_T"],0)
        self.assertEqual(x["B1_T_quantiles"],sorted(x["B1_T_quantiles"]))
    def test_invalid(self):
        with self.assertRaises(ValueError): thermal_magnon_to_b1(2.87e9,600,300,1e-9)
if __name__=="__main__": unittest.main()
