import os
from typing import List

def scan_for_git_repos(path: str) -> List[str]:
    """
    Scan the given path for folders containing git repositories one level deep.

    :param path: Path to the directory to scan
    :return: List of directories containing .git folders
    :raises ValueError: If the input path is not a valid directory
    """
    if not os.path.isdir(path):
        raise ValueError(f"The path '{path}' is not a valid directory.")

    git_repos = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path) and '.git' in os.listdir(item_path):
            git_repos.append(item_path)

    return git_repos