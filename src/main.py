import sched
import threading
import time
import logging
from typing import List, Optional
from src.get_env import load_environment_variables

# Setup logging with a specified level and format
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Create a scheduler instance to manage timed tasks
scheduler = sched.scheduler(time.time, time.sleep)

def log_scheduled_task():
    """Logs the scheduled task execution and sets up the next execution."""
    logging.info("Scheduled task executed.")
    # Schedule the next execution of this task for 5 seconds later
    scheduler.enter(5, 1, log_scheduled_task)

def start_scheduler(run_frequency: int, stop_event: threading.Event) -> None:
    """Starts the scheduler with the specified run frequency."""
    # Initial call to schedule the first task
    scheduler.enter(run_frequency, 1, log_scheduled_task)
    # Continuously run the scheduler until the stop_event is triggered
    while not stop_event.is_set():
        scheduler.run(blocking=False)

def main(should_run: bool = True, run_frequency: Optional[int] = None,
         project_folder: Optional[str] = None, access_key: Optional[str] = None) -> None:
    """
    Main function that orchestrates the program operations.

    Args:
        should_run (bool): A flag to indicate whether the loop should continue running.
    """
    # Load environment variables, fallback to default if not provided
    if run_frequency is None or project_folder is None or access_key is None:
        run_frequency, project_folder, access_key = load_environment_variables()
    
    # Log the configurations being used in the program
    logging.info(f"Run Frequency: {run_frequency}")
    logging.info(f"Project Folder: {project_folder}")
    logging.info(f"Git Access Key: {access_key}")

    # Create a stop event to signal the scheduler to stop
    stop_event = threading.Event()
    # Create and start a new thread to handle the execution of the scheduler
    scheduler_thread = threading.Thread(target=start_scheduler, args=(run_frequency, stop_event))
    scheduler_thread.start()

    try:
        # Main loop that executes while should_run is set to True
        while should_run:
            logging.info(f"Executing pull_repositories at interval of {10} seconds.")
            time.sleep(10)
    except KeyboardInterrupt:
        # Signal to stop the scheduler thread on a keyboard interrupt
        stop_event.set()
        logging.info("Program interrupted. Exiting gracefully.")
    finally:
        # Wait for the scheduler thread to finish gracefully
        scheduler_thread.join()
        logging.info("Scheduler stopped. Exiting gracefully.")

if __name__ == "__main__":
    main()  # Execute the main function when the script is run