import subprocess
import docker

class DockerHandler:
    def __init__(self, compose_file_path):
        self.compose_file_path = compose_file_path
        self.client = docker.from_env()

    def _run_compose_command(self, command):
        """Run a docker-compose command and return the output."""
        try:
            result = subprocess.run(
                ["docker-compose", "-f", self.compose_file_path] + command,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"  # Return error output if command fails

    def build(self):
        """Build docker-compose images."""
        return self._run_compose_command(["build"])

    def start(self):
        """Start docker-compose services."""
        return self._run_compose_command(["up", "-d"])

    def stop(self):
        """Stop docker-compose services."""
        return self._run_compose_command(["down"])

    def list_running_containers(self):
        """List currently running containers."""
        containers = self.client.containers.list()
        return [container.name for container in containers]