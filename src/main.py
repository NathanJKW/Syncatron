import asyncio
import logging
from typing import List, Optional
from src.get_env import load_environment_variables
from src.filesystem_handler import scan_for_git_repos
from src.git_handler import pull_repositories
from src.docker_handler import handle_docker_operations

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def log_scheduled_task(run_frequency: int, project_folder: str, access_key: str) -> None:
    """Logs the scheduled task execution."""
    logging.info(f"Scanning project folder '{project_folder}' for git repositories.")
    found_repos = scan_for_git_repos(project_folder)

    logging.info(f"Found {len(found_repos)} git repositories. Trying updates")
    updated_repos = await asyncio.to_thread(pull_repositories, access_key, found_repos)

    if not updated_repos:
        logging.info("No git repositories with changes. Skipping Docker container rebuild.")
    else:
        logging.info(f"{len(updated_repos)} git repositories with changes. Rebuilding Docker containers.")
        for repo in updated_repos:
            await asyncio.to_thread(handle_docker_operations, repo)

async def scheduler(run_frequency: int, project_folder: str, access_key: str) -> None:
    while True:
        await log_scheduled_task(run_frequency, project_folder, access_key)
        await asyncio.sleep(run_frequency)  # Use asyncio sleep to avoid blocking

async def main(run_frequency: Optional[int] = None, project_folder: Optional[str] = None,
         access_key: Optional[str] = None) -> None:
    """
    Main function that orchestrates the program operations.
    """
    # Load environment variables if not provided
    if run_frequency is None or project_folder is None or access_key is None:
        run_frequency, project_folder, access_key = load_environment_variables()

    logging.info(f"Run Frequency: {run_frequency}")
    logging.info(f"Project Folder: {project_folder}")
    logging.info(f"Git Access Key: {access_key}")

    # Start the scheduler
    await scheduler(run_frequency, project_folder, access_key)

if __name__ == "__main__":
    asyncio.run(main())  # Execute the main function using asyncio's event loop