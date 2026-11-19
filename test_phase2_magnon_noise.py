import unittest
from phase2_magnon_noise import simulate_noise,thermal_null_control
class TestNoise(unittest.TestCase):
    def test_no_drive_no_flip(self):
        for t in (300,600):
            self.assertAlmostEqual(thermal_null_control(t,200)["mean_excited"],0,places=12)
    def test_ideal_pi(self):
        self.assertAlmostEqual(simulate_noise(300,100,base_noise_hz=0)["mean_excited"],1,places=10)
    def test_unitarity(self):
        for t in (300,600):
            self.assertAlmostEqual(simulate_noise(t,200)["mean_norm"],1,places=10)
    def test_reproducible(self):
        self.assertEqual(simulate_noise(300,200,seed=3),simulate_noise(300,200,seed=3))
    def test_noise_growth(self):
        self.assertGreater(simulate_noise(600,100)["noise_std_hz"],simulate_noise(300,100)["noise_std_hz"])
    def test_invalid(self):
        with self.assertRaises(ValueError): simulate_noise(0)
if __name__=="__main__": unittest.main()
