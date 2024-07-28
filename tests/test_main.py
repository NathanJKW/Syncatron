import unittest
from src.main import validate_directories

class TestScanForMain(unittest.TestCase):

    def test_validate_directories_valid(self):
        directories = ['/path/to/repo1', '/path/to/repo2']
        try:
            validate_directories(directories)
        except ValueError:
            self.fail("validate_directories raised ValueError unexpectedly!")

    def test_validate_directories_invalid(self):
        directories = ['/path/to/repo1', 123]  # One invalid entry
        with self.assertRaises(ValueError) as excinfo:
            validate_directories(directories)
        self.assertIn("should be of type str", str(excinfo.exception))

if __name__ == '__main__':
    unittest.main()