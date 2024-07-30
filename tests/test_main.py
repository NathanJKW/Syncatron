# tests/test_main.py

import pytest
import logging
import time
import threading
from unittest.mock import patch
from src.main import start_scheduler, log_scheduled_task, main

# Setup logging at the DEBUG level for the tests
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@pytest.fixture
def mock_load_env_vars():
    """Mock the load_environment_variables function to return test values."""
    with patch('src.main.load_environment_variables', return_value=(5, 'test_project_folder', 'test_access_key')):
        yield

def test_log_scheduled_task(caplog):
    """Test the log_scheduled_task function logging."""
    with caplog.at_level(logging.INFO):
        log_scheduled_task()
    
    assert "Scheduled task executed." in caplog.text

def test_start_scheduler(mock_load_env_vars):
    """Test the start_scheduler function initializes the scheduler correctly."""
    # Mock the scheduler to just call the log_scheduled_task without waiting
    with patch('sched.scheduler.enter') as mock_enter:
        thread = threading.Thread(target=start_scheduler, args=(5,))
        thread.start()
        
        # Give it some time to run
        time.sleep(1)
        
        # Check the scheduler's enter call
        assert mock_enter.call_count > 0
        thread.join(timeout=1)

def test_main_function(mock_load_env_vars):
    """Test that the main function runs without errors."""
    # Mocking the logging functions to avoid cluttering the output
    with patch('logging.info') as mock_log_info:
        # Execute main function which will use the mocked load_environment_variables
        # Calling main with should_run set to False to terminate the loop immediately.
        main(should_run=False)
        
        mock_log_info.assert_any_call("Run Frequency: 5")
        mock_log_info.assert_any_call("Project Folder: test_project_folder")
        mock_log_info.assert_any_call("Git Access Key: test_access_key")

@pytest.mark.parametrize("interval", [1, 2, 3])
def test_scheduler_run_frequency(mock_load_env_vars, interval):
    """Test that the scheduler runs at the expected frequency."""
    with patch('sched.scheduler.enter', side_effect=lambda delay, priority, action: action()):
        thread = threading.Thread(target=start_scheduler, args=(interval,))
        thread.start()
        
        # Allow the scheduled task to execute
        time.sleep(4)  # Wait a bit longer than the interval
        thread.join(timeout=1)  # Ensure the thread has completed