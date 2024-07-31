# test_docker_operations.py

import pytest
import subprocess
import logging
import os
from src.docker_handler import (
    get_docker_compose_file,
    teardown_container,
    rebuild_container,
    start_container,
    remove_unused_images,
    run_command,
    handle_docker_operations,
)

@pytest.fixture(scope='module', autouse=True)
def configure_logging():
    logging.basicConfig(level=logging.INFO)

@pytest.fixture
def mock_docker_compose_file(monkeypatch):
    # Mock the os.path.exists function to always return True for the docker-compose file
    def exists_mock(path):
        return path.endswith("docker-compose.yml")

    monkeypatch.setattr(os.path, "exists", exists_mock)
    yield "/mock/path"  # This will simulate a valid path where the docker-compose file is expected

def test_get_docker_compose_file_valid(mock_docker_compose_file):
    assert get_docker_compose_file(mock_docker_compose_file) == os.path.join(mock_docker_compose_file, "docker-compose.yml")

def test_get_docker_compose_file_invalid_path():
    with pytest.raises(ValueError, match="Path cannot be empty"):
        get_docker_compose_file("")

def test_teardown_container_valid(mock_docker_compose_file, monkeypatch):
    def mock_run(command, shell, text=True, capture_output=True):
        return subprocess.CompletedProcess(args=command, returncode=0)

    monkeypatch.setattr(subprocess, "run", mock_run)
    assert teardown_container(mock_docker_compose_file)  # Should return True

def test_rebuild_container_valid(mock_docker_compose_file, monkeypatch):
    def mock_run(command, shell, text=True, capture_output=True):
        return subprocess.CompletedProcess(args=command, returncode=0)

    monkeypatch.setattr(subprocess, "run", mock_run)
    assert rebuild_container(mock_docker_compose_file)  # Should return True

def test_start_container_valid(mock_docker_compose_file, monkeypatch):
    def mock_run(command, shell, text=True, capture_output=True):
        return subprocess.CompletedProcess(args=command, returncode=0)

    monkeypatch.setattr(subprocess, "run", mock_run)
    assert start_container(mock_docker_compose_file)  # Should return True

def test_remove_unused_images(mock_docker_compose_file, monkeypatch):
    def mock_run(command, shell, text=True, capture_output=True):
        return subprocess.CompletedProcess(args=command, returncode=0)

    monkeypatch.setattr(subprocess, "run", mock_run)
    assert remove_unused_images()  # Should return True

def test_run_command_valid(monkeypatch):
    def mock_run(command, shell, text=True, capture_output=True):
        return subprocess.CompletedProcess(args=command, returncode=0, stdout="Test Output", stderr="")

    monkeypatch.setattr(subprocess, "run", mock_run)
    assert run_command("echo Test") == ("Test Output", "", 0)  # Matches the mocked output

def test_handle_docker_operations_invalid_path(caplog):
    handle_docker_operations("")
    assert "Invalid path provided. Exiting." in caplog.text