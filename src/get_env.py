import os
import logging
from typing import Tuple, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_environment_variable(var_name: str) -> Optional[str]:
    """
    Retrieve the environment variable by name.
    
    Args:
        var_name (str): The name of the environment variable.

    Returns:
        Optional[str]: The value of the environment variable or None.
    """
    return os.getenv(var_name)

def validate_positive_integer(value: Optional[str], var_name: str) -> int:
    """
    Validate if the string value is a positive integer.
    
    Args:
        value (Optional[str]): The value to validate.
        var_name (str): The name of the variable for logging purposes.
        
    Returns:
        int: The validated positive integer.
    
    Raises:
        ValueError: If value is not a positive integer.
    """
    if not value or not value.isdigit():
        logger.error(f"{var_name} is not set or not a positive integer.")
        raise ValueError(f"{var_name} must be set to a positive integer.")
    
    result = int(value)
    if result <= 0:
        logger.error(f"{var_name} must be a positive integer.")
        raise ValueError(f"{var_name} must be a positive integer.")
    
    return result

def validate_environment_variables() -> Tuple[int, str, str]:
    """
    Validate critical environment variables.

    Returns:
        Tuple[int, str, str]: A tuple containing run_frequency, project_folder, and access_key.

    Raises:
        EnvironmentError: If any required environment variable is not set.
    """
    project_folder = get_environment_variable('PROJECT_FOLDER')
    access_key = get_environment_variable('GIT_ACCESS_KEY')

    if project_folder is None:
        logger.error("PROJECT_FOLDER is not set.")
        raise EnvironmentError("PROJECT_FOLDER must be set.")

    if access_key is None:
        logger.error("GIT_ACCESS_KEY is not set.")
        raise EnvironmentError("GIT_ACCESS_KEY must be set.")

    run_frequency_raw = get_environment_variable('RUN_FREQUENCY')
    run_frequency = validate_positive_integer(run_frequency_raw, 'RUN_FREQUENCY')

    logger.info(f"Loaded environment variables successfully.")
    
    return run_frequency, project_folder, access_key

def load_environment_variables() -> Tuple[int, str, str]:
    """
    Load and validate environment variables, returning them for further use.
    """
    try:
        return validate_environment_variables()
    except Exception:
        logger.exception("An error occurred while loading environment variables.")
        raise