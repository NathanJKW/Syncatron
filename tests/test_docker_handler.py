import unittest
from unittest.mock import patch, MagicMock
from src.docker_handler import DockerHandler  # Adjust this import according to your project structure

class TestDockerHandler(unittest.TestCase):
    def setUp(self):
        # Set up a testing environment
        self.compose_file_path = "path/to/your/docker-compose.yml"
        self.docker_handler = DockerHandler(self.compose_file_path)

    @patch('subprocess.run')
    def test_build(self, mock_run):
        mock_run.return_value.stdout = "Images built successfully"
        result = self.docker_handler.build()
        mock_run.assert_called_once_with(
            ["docker-compose", "-f", self.compose_file_path, "build"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(result, "Images built successfully")

    @patch('subprocess.run')
    def test_start(self, mock_run):
        mock_run.return_value.stdout = "Services started"
        result = self.docker_handler.start()
        mock_run.assert_called_once_with(
            ["docker-compose", "-f", self.compose_file_path, "up", "-d"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(result, "Services started")

    @patch('subprocess.run')
    def test_stop(self, mock_run):
        mock_run.return_value.stdout = "Services stopped"
        result = self.docker_handler.stop()
        mock_run.assert_called_once_with(
            ["docker-compose", "-f", self.compose_file_path, "down"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertEqual(result, "Services stopped")

    @patch('src.docker_handler.docker.from_env')  # Mocking the from_env method
    def test_list_running_containers(self, mock_from_env):
        mock_container = MagicMock()
        mock_container.name = "test_container"
        mock_from_env.return_value.containers.list.return_value = [mock_container]

        # Reinitialize the DockerHandler to ensure it uses the mocked from_env
        docker_handler = DockerHandler(self.compose_file_path)

        result = docker_handler.list_running_containers()  # Call on the newly created instance
        mock_from_env.assert_called_once()  # This should now work as expected
        self.assertEqual(result, ["test_container"])