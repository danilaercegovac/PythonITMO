import math
import unittest

from integrate_py import integrate


class TestIntegrate(unittest.TestCase):
    def test_known_integral_sin(self):
        # ∫[0,π] sin(x) dx = 2
        val = integrate(math.sin, 0.0, math.pi, n_iter=300_000)
        self.assertAlmostEqual(val, 2.0, places=4)

    def test_stability_with_iterations(self):
        # Check if error decrease when n_iter increase
        # ∫[0,1] x^2 dx = 1/3
        f = lambda x: x * x
        exact = 1.0 / 3.0

        v1 = integrate(f, 0.0, 1.0, n_iter=10_000)
        v2 = integrate(f, 0.0, 1.0, n_iter=200_000)

        err1 = abs(v1 - exact)
        err2 = abs(v2 - exact)

        self.assertGreater(err1, err2)
        self.assertAlmostEqual(v2, exact, places=4)


if __name__ == "__main__":
    unittest.main()
