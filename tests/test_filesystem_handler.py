import pytest
import os
import tempfile
import shutil
from src.filesystem_handler import scan_for_git_repos

@pytest.fixture
def setup_git_repos():
    """
    Create a temporary directory with some git repositories for testing.
    """
    temp_dir = tempfile.mkdtemp()
    os.makedirs(os.path.join(temp_dir, "repo1/.git"))
    os.makedirs(os.path.join(temp_dir, "repo2/.git"))
    os.makedirs(os.path.join(temp_dir, "not_a_git_repo"))
    
    yield temp_dir

    shutil.rmtree(temp_dir)

def test_scan_for_valid_git_repos(setup_git_repos):
    """
    Test scanning for valid git repositories.
    """
    repos = scan_for_git_repos(setup_git_repos)
    assert len(repos) == 2
    assert all(repo in repos for repo in [os.path.join(setup_git_repos, "repo1"), os.path.join(setup_git_repos, "repo2")])

def test_scan_for_invalid_directory():
    """
    Test scanning for an invalid directory.
    """
    with pytest.raises(ValueError):
        scan_for_git_repos("invalid/path/to/dir")