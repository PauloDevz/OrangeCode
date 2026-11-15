import unittest
from calculadora import add, sub, mul, div

class TestCalculadora(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
    def test_sub(self):
        self.assertEqual(sub(5, 3), 2)
        self.assertEqual(sub(0, 5), -5)
    def test_mul(self):
        self.assertEqual(mul(4, 3), 12)
        self.assertEqual(mul(-2, 3), -6)
    def test_div(self):
        self.assertEqual(div(10, 2), 5)
        self.assertAlmostEqual(div(7, 3), 7/3)
    def test_div_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            div(5, 0)

if __name__ == '__main__':
    unittest.main()
