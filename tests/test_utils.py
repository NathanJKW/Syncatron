import unittest
from src.utils import heart

class TestUtils(unittest.TestCase):
    def test_heart(self):
        num1 = 1
        num2 = 1
        expected = 2
        self.assertEqual(heart(num1, num2), expected)