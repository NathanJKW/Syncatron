import time
import logging
from typing import List
from get_env import load_environment_variables

# Setup logging configuration investigate proper logging
#logging.basicConfig(
#    filename='git_pull.log',
#    level=logging.INFO,
#    format='%(asctime)s - %(levelname)s - %(message)s'
#)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main(interval: int, access_token: str, directories: List[str]) -> None:
    """
    Main function that orchestrates the program.

    Args:
        interval (int): The interval in seconds between each execution.
        access_token (str): Personal access token for authentication.
        directories (List[str]): List of directory paths to perform git pull on.
    """
    # Load environment variables
    run_frequency, project_folder, access_key = load_environment_variables()
    
    # Using the loaded environment variables
    logger.info(f"Run Frequency: {run_frequency}")
    logger.info(f"Project Folder: {project_folder}")
    logger.info(f"Git Access Key: {access_key}")


    # todo - implement the main function with a scheduler
    try:
        while True:
            logging.info(f"Executing pull_repositories at interval of {interval} seconds.")
            time.sleep(interval)
            logging.info(f"Interval of {interval} seconds has elapsed. Re-executing.")
    except KeyboardInterrupt:
        logging.info("Program interrupted. Exiting gracefully.")