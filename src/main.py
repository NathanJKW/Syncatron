import time
import configparser
import logging
from typing import List
from git import Repo, GitCommandError

# Setup logging configuration
logging.basicConfig(
    filename='git_pull.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_directories(directories: List[str]) -> None:
    """
    Validate the provided directories.

    Args:
        directories (List[str]): List of directory paths to validate.
    
    Raises:
        ValueError: If a directory is invalid or not a string.
    """
    for directory in directories:
        if not isinstance(directory, str):
            raise ValueError(f"Directory should be of type str: {directory}")
        # Additional checks can be added here (e.g., check existence)

def pull_repositories(access_token: str, directories: List[str]) -> None:
    """
    Perform a git pull on a list of directories using the provided access token.

    Args:
        access_token (str): Personal access token for authentication.
        directories (List[str]): List of directory paths to perform git pull on.

    Raises:
        ValueError: If a directory is invalid or git operation fails.
    """
    validate_directories(directories)

    for directory in directories:
        try:
            logging.info(f"Pulling repository in directory: {directory}")
            repo = Repo(directory)
            origin = repo.remotes.origin
            # Set up environment to pass the access token for git pull
            with repo.git.custom_environment(GIT_ASKPASS="echo", GIT_PASSWORD=access_token):
                origin.pull()
            logging.info(f"Successfully pulled in {directory}")
        except GitCommandError as e:
            logging.error(f"Git command error in {directory}. Error: {e}")
            raise ValueError(f"Error pulling in {directory}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error in {directory}. Error: {e}")
            raise ValueError(f"Unexpected error pulling in {directory}: {e}")

def main(interval: int, access_token: str, directories: List[str]) -> None:
    """
    Main function that orchestrates the program.

    Args:
        interval (int): The interval in seconds between each execution.
        access_token (str): Personal access token for authentication.
        directories (List[str]): List of directory paths to perform git pull on.
    """
    if not isinstance(interval, int) or interval <= 0:
        raise ValueError("Interval should be a positive integer.")
    
    validate_directories(directories)

    try:
        while True:
            logging.info(f"Executing pull_repositories at interval of {interval} seconds.")
            pull_repositories(access_token, directories)
            time.sleep(interval)
            logging.info(f"Interval of {interval} seconds has elapsed. Re-executing.")
    except KeyboardInterrupt:
        logging.info("Program interrupted. Exiting gracefully.")