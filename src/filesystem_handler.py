import os
from typing import List
import logging

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def scan_for_git_repos(path: str) -> List[str]:
    """
    Scan the given path for folders containing git repositories one level deep.

    :param path: Path to the directory to scan
    :return: List of directories containing .git folders
    :raises ValueError: If the input path is not a valid directory
    """
    # Validating the input directory
    if not os.path.isdir(path):
        logging.error(f"The path '{path}' is not a valid directory.")
        raise ValueError(f"The path '{path}' is not a valid directory.")

    git_repos = []
    # Iterating over items in the provided directory
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        # Check if the item is a directory and contains a .git folder
        if os.path.isdir(item_path):
            if '.git' in os.listdir(item_path):
                git_repos.append(item_path)
                logging.info(f"Found git repository: {item_path}")

    logging.info(f"Total git repositories found: {len(git_repos)}")
    return git_repos