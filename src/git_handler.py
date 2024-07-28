import logging
from typing import List
from git import Repo, GitCommandError

logger = logging.getLogger(__name__)

def pull_repositories(access_token: str, directories: List[str]) -> List[str]:
    """
    Perform a git pull on a list of directories using the provided access token.

    Args:
        access_token (str): Personal access token for authentication.
        directories (List[str]): List of directory paths to perform git pull on.

    Returns:
        List[str]: List of directories where there was an update.

    Raises:
        ValueError: If a directory is invalid or git operation fails.
    """
    updated_directories = []

    for directory in directories:
        try:
            repo = Repo(directory)
            origin = repo.remotes.origin
            with repo.git.custom_environment(GIT_ASKPASS="echo", GIT_PASSWORD=access_token):
                result = origin.pull()
                if any(item.flags != 4 for item in result):  # Check if there was an update
                    updated_directories.append(directory)
            logger.info(f"Successfully pulled in {directory}")
        except GitCommandError as e:
            logger.info(f"Git command error in {directory}: {e}")
        except Exception as e:
            logger.info(f"Error in {directory}: {e}")

    return updated_directories