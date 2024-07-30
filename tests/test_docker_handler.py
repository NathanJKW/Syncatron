import pytest
from src.docker_handler import run_command

def test_run_command_success():
    output, error, exit_code = run_command("echo Hello, World!")
    assert exit_code == 0
    assert output.strip() == "Hello, World!"
    assert error == ""

def test_run_command_failure():
    output, error, exit_code = run_command("non_existing_command")
    assert exit_code != 0
    assert "non_existing_command" in error.lower()  # Adjust based on the actual error message

def test_run_empty_command():
    with pytest.raises(ValueError, match="Command cannot be empty"):
        run_command("")