# docker_operations.py

import os
import subprocess
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_docker_compose_file(path: str) -> str:
    """Get the path to the docker-compose.yml file.
    
    Args:
        path (str): The path to the directory containing the docker-compose.yml file.
    
    Returns:
        str: The path to the docker-compose.yml file.

    Raises:
        ValueError: If the path is empty or the docker-compose.yml file is not found.
    """
    if not path:
        logging.error(f"Invalid path: {path}")
        raise ValueError("Path cannot be empty")
    
    docker_compose_file = os.path.join(path, "docker-compose.yml")
    
    if not os.path.exists(docker_compose_file):
        logging.error(f"No docker-compose.yml file found in path: {path}")
        raise FileNotFoundError("docker-compose.yml not found")

    return docker_compose_file

def teardown_container(path: str) -> bool:
    """Stop and remove the Docker container.
    
    Args:
        path (str): The path to the directory containing the docker-compose.yml file.
    
    Returns:
        bool: True if the container was successfully stopped and removed, False otherwise.
    """
    try:
        docker_compose_file = get_docker_compose_file(path)

        command = f"docker compose -f {docker_compose_file} down"
        output, error, exit_code = run_command(command)

        if exit_code == 0:
            logging.info("Container stopped and removed successfully")
            return True

        logging.error(f"Failed to stop and remove container: {error}")
        return False
    except (ValueError, FileNotFoundError) as e:
        logging.error(e)
        return False

def rebuild_container(path: str) -> bool:
    """Rebuild the Docker container.
    
    Args:
        path (str): The path to the directory containing the docker-compose.yml file.
    
    Returns:
        bool: True if the container was successfully rebuilt, False otherwise.
    """
    try:
        docker_compose_file = get_docker_compose_file(path)

        command = f"docker compose -f {docker_compose_file} build --no-cache"
        output, error, exit_code = run_command(command)

        if exit_code == 0:
            logging.info("Container rebuilt successfully")
            return True

        logging.error(f"Failed to rebuild container: {error}")
        return False
    except (ValueError, FileNotFoundError) as e:
        logging.error(e)
        return False

def start_container(path: str) -> bool:
    """Start the Docker container.
    
    Args:
        path (str): The path to the directory containing the docker-compose.yml file.
    
    Returns:
        bool: True if the container was successfully started, False otherwise.
    """
    try:
        docker_compose_file = get_docker_compose_file(path)

        command = f"docker compose -f {docker_compose_file} up -d"
        output, error, exit_code = run_command(command)

        if exit_code == 0:
            logging.info("Container started successfully")
            return True

        logging.error(f"Failed to start container: {error}")
        return False
    except (ValueError, FileNotFoundError) as e:
        logging.error(e)
        return False

def remove_unused_images() -> bool:
    """Remove unused Docker images.
    
    Returns:
        bool: True if the unused images were successfully removed, False otherwise.
    """
    command = "docker image prune -f"
    output, error, exit_code = run_command(command)

    if exit_code == 0:
        logging.info("Unused images removed successfully")
        return True

    logging.error(f"Failed to remove unused images: {error}")
    return False

def run_command(command: str):
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
    
def handle_docker_operations(path: str) -> None:
    """Handle Docker operations for the specified path.
    
    Args:
        path (str): The path to the directory containing the docker-compose.yml file.
    """
    if not path:
        logging.error("Invalid path provided. Exiting.")
        return
    
    if not teardown_container(path):
        logging.error("Failed to stop and remove the container. Exiting.")
        return
    
    if not rebuild_container(path):
        logging.error("Failed to rebuild the container. Exiting.")
        return
    
    if not start_container(path):
        logging.error("Failed to start the container. Exiting.")
        return
    
    if not remove_unused_images():
        logging.error("Failed to remove unused images. Exiting.")
        return
    
    logging.info("Docker operations completed successfully")