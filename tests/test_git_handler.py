import unittest
from unittest.mock import patch, MagicMock
from src.git_handler import pull_repositories

class TestPullRepositories(unittest.TestCase):

    @patch('src.git_handler.Repo')
    def test_successful_pull(self, mock_repo: MagicMock):
        mock_repo.return_value.remotes.origin.pull.return_value = [MagicMock(flags=0)]
        directories = ['/valid/repo1', '/valid/repo2']
        updates = pull_repositories('dummy_access_token', directories)
        self.assertEqual(updates, directories)

    @patch('src.git_handler.Repo')
    def test_no_updates(self, mock_repo: MagicMock):
        mock_repo.return_value.remotes.origin.pull.return_value = [MagicMock(flags=4)]
        directories = ['/valid/repo1']
        updates = pull_repositories('dummy_access_token', directories)
        self.assertEqual(updates, [])

    @patch('src.git_handler.Repo')
    def test_invalid_directory(self, mock_repo: MagicMock):
        mock_repo.side_effect = Exception("Invalid directory")
        directories = ['/invalid/repo']
        with self.assertLogs(level='INFO') as log:
            updates = pull_repositories('dummy_access_token', directories)
            self.assertIn("INFO:src.git_handler:Error in /invalid/repo: Invalid directory", log.output)
            self.assertEqual(updates, [])

    @patch('src.git_handler.Repo')
    def test_git_command_error(self, mock_repo: MagicMock):
        mock_repo.return_value.remotes.origin.pull.side_effect = Exception("Git command error")
        directories = ['/valid/repo']
        with self.assertLogs(level='INFO') as log:
            updates = pull_repositories('dummy_access_token', directories)
            self.assertIn("INFO:src.git_handler:Error in /valid/repo: Git command error", log.output)
            self.assertEqual(updates, [])

    def test_empty_directory_list(self):
        directories = []
        updates = pull_repositories('dummy_access_token', directories)
        self.assertEqual(updates, [])

if __name__ == '__main__':
    unittest.main()