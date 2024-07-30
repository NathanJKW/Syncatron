import unittest
import os
import tempfile
from src.filesystem_handler import scan_for_git_repos

class TestScanForGitRepos(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for the tests
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        # Cleanup the temporary directory
        self.test_dir.cleanup()

    def test_valid_directory_with_git_repos(self):
        # Create a directory structure with .git folders one level deep
        os.makedirs(os.path.join(self.test_dir.name, 'repo1', '.git'))
        os.makedirs(os.path.join(self.test_dir.name, 'repo2', '.git'))
        
        result = scan_for_git_repos(self.test_dir.name)
        expected = [
            os.path.join(self.test_dir.name, 'repo1'),
            os.path.join(self.test_dir.name, 'repo2')
        ]
        
        self.assertCountEqual(result, expected)

    def test_valid_directory_without_git_repos(self):
        # Create a directory structure without .git folders
        os.makedirs(os.path.join(self.test_dir.name, 'folder1'))
        os.makedirs(os.path.join(self.test_dir.name, 'folder2'))
        
        result = scan_for_git_repos(self.test_dir.name)
        expected = []
        
        self.assertEqual(result, expected)

    def test_invalid_directory_path(self):
        with self.assertRaises(ValueError):
            scan_for_git_repos('/invalid/path')

    def test_nested_git_repos_not_detected(self):
        # Create a directory structure with nested .git folders
        os.makedirs(os.path.join(self.test_dir.name, 'outer', 'inner', '.git'))
        
        result = scan_for_git_repos(self.test_dir.name)
        expected = []
        
        self.assertEqual(result, expected)