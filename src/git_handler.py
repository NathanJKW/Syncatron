import logging
from typing import List
from git import Repo, GitCommandError

logger = logging.getLogger(__name__)

def add_token_to_remote_url(url, token):
    """
    Add the access token to the remote URL for authentication.

    :param url: The original remote URL.
    :param token: The access token to be added to the URL.
    :return: The remote URL with the access token embedded.
    """
    protocol, base_url = url.split('://')
    if '@' in base_url:
        base_url = base_url.split('@')[-1]
    
    return f"{protocol}://{token}@{base_url}"

def pull_repositories(access_token: str, directories: List[str]) -> List[str]:
    """
    Perform a git pull on a list of directories using the provided personal access token.

    Args:
        access_token (str): Personal access token for authentication.
        directories (List[str]): List of directory paths to perform git pull on.
        repo_url_template (str): Template for the git URL, where {token} will be replaced by the access token.

    Returns:
        List[str]: List of directories where there was an update.

    Raises:
        ValueError: If a directory is invalid or git operation fails.
    """
    updated_directories = []

    for directory in directories:
        try:
            # Get the repo and its origin URL
            repo = Repo(directory)
            origin = repo.remotes.origin
            
            # Construct the new remote URL with the personal access token
            new_origin_url = add_token_to_remote_url(token=access_token, url=origin.url)
            origin.set_url(new_origin_url)
            # Perform the git pull
            result = origin.pull()
            
            # Check if there were updates based on new_count
            updates_detected = False
            for fetch_info in result:
                if fetch_info.new_count > 0:  # Check if there are new commits
                    updated_directories.append(directory)
                    updates_detected = True
                    break  # We found an update, no need to check further
                
            if updates_detected:
                logger.info(f"Updates detected in {directory}.")
            else:
                logger.info(f"No updates detected in {directory}.")
            
        except GitCommandError as e:
            logger.info(f"Git command error in {directory}: {e}")
        except Exception as e:
            logger.info(f"Error in {directory}: {e}")

    return updated_directories