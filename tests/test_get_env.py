import os
import pytest
from unittest.mock import patch
from src.get_env import load_environment_variables

# Sample test cases for environment variable loading
def test_load_environment_variables_valid(monkeypatch):
    """Test successful loading of valid environment variables."""
    monkeypatch.setenv('RUN_FREQUENCY', '5')
    monkeypatch.setenv('PROJECT_FOLDER', '/path/to/project')
    monkeypatch.setenv('GIT_ACCESS_KEY', 'some_access_key')
    
    run_frequency, project_folder, access_key = load_environment_variables()
    
    assert run_frequency == 5
    assert project_folder == '/path/to/project'
    assert access_key == 'some_access_key'

def test_load_environment_variables_missing_run_frequency(monkeypatch):
    """Test handling of missing RUN_FREQUENCY."""
    monkeypatch.setenv('PROJECT_FOLDER', '/path/to/project')
    monkeypatch.setenv('GIT_ACCESS_KEY', 'some_access_key')

    with pytest.raises(ValueError, match="RUN_FREQUENCY must be set to a positive integer."):
        load_environment_variables()

def test_load_environment_variables_invalid_run_frequency(monkeypatch):
    """Test handling of invalid RUN_FREQUENCY (not a positive integer)."""
    monkeypatch.setenv('RUN_FREQUENCY', '0')
    monkeypatch.setenv('PROJECT_FOLDER', '/path/to/project')
    monkeypatch.setenv('GIT_ACCESS_KEY', 'some_access_key')

    with pytest.raises(ValueError, match="RUN_FREQUENCY must be a positive integer."):
        load_environment_variables()

def test_load_environment_variables_missing_project_folder(monkeypatch):
    """Test handling of missing PROJECT_FOLDER."""
    monkeypatch.setenv('RUN_FREQUENCY', '5')
    monkeypatch.setenv('GIT_ACCESS_KEY', 'some_access_key')

    with pytest.raises(EnvironmentError, match="PROJECT_FOLDER must be set."):
        load_environment_variables()

def test_load_environment_variables_missing_access_key(monkeypatch):
    """Test handling of missing GIT_ACCESS_KEY."""
    monkeypatch.setenv('RUN_FREQUENCY', '5')
    monkeypatch.setenv('PROJECT_FOLDER', '/path/to/project')

    with pytest.raises(EnvironmentError, match="GIT_ACCESS_KEY must be set."):
        load_environment_variables()

def test_load_environment_variables_invalid_run_frequency_type(monkeypatch):
    """Test handling of invalid RUN_FREQUENCY (not a number)."""
    monkeypatch.setenv('RUN_FREQUENCY', 'invalid_number')
    monkeypatch.setenv('PROJECT_FOLDER', '/path/to/project')
    monkeypatch.setenv('GIT_ACCESS_KEY', 'some_access_key')

    with pytest.raises(ValueError, match="RUN_FREQUENCY must be set to a positive integer."):
        load_environment_variables()