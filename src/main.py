import sched
import threading
import time
import logging
from typing import List
from src.get_env import load_environment_variables

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a scheduler instance
scheduler = sched.scheduler(time.time, time.sleep)

# Define a scheduled task that logs every 5 seconds
def log_scheduled_task():
    """Logs the scheduled task execution."""
    logging.info("Scheduled task executed.")
    # Schedule the next execution after 5 seconds
    scheduler.enter(5, 1, log_scheduled_task)

# Start the scheduler in a separate thread
def start_scheduler(run_frequency: int) -> None:
    """Starts the scheduler with the given run frequency."""
    scheduler.enter(run_frequency, 1, log_scheduled_task)  # Initial call to schedule
    scheduler.run()

def main(should_run: bool = True) -> None:
    """
    Main function that orchestrates the program.

    Args:
        should_run (bool): A flag to indicate whether the loop should continue running.
    """
    # Load environment variables
    run_frequency, project_folder, access_key = load_environment_variables()
    
    # Using the loaded environment variables
    logging.info(f"Run Frequency: {run_frequency}")
    logging.info(f"Project Folder: {project_folder}")
    logging.info(f"Git Access Key: {access_key}")
    
    # Start the scheduler thread
    scheduler_thread = threading.Thread(target=start_scheduler, args=(run_frequency,))
    scheduler_thread.start()

    try:
        while should_run:
            # Allow other operations to run
            logging.info(f"Executing pull_repositories at interval of {10} seconds.")
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Program interrupted. Exiting gracefully.")

if __name__ == "__main__":
    main()