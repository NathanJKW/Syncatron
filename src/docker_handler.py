import subprocess
import logging
import sys

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command):
    """Run a shell command and return the output, error (if any), and exit status.
    
    Args:
        command (str): The command to be executed.

    Returns:
        tuple: A tuple containing the output, error, and exit code.
    
    Raises:
        ValueError: If the command is empty.
    """
    
    if not command:
        raise ValueError("Command cannot be empty")
    
    logging.info(f"Running command: {command}")

    try:
        # Running the command and capturing output & error
        result = subprocess.run(command, shell=True, text=True, capture_output=True)

        # Logging the output and error
        if result.stdout:
            logging.info(f"Output:\n{result.stdout}")
        
        if result.stderr:
            logging.error(f"Error:\n{result.stderr}")

        return result.stdout, result.stderr, result.returncode

    except Exception as e:
        logging.error(f"An exception occurred: {str(e)}")
        return None, str(e), -1