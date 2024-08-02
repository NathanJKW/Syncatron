# Dockerfile

# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file first to leverage Docker caching
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y git && apt-get clean
# Copy the rest of the application code
COPY . .

# Set environment variables (optional)
# ENV PROJECT_FOLDER=/path/to/project
# ENV GIT_ACCESS_KEY=your_access_key
# ENV RUN_FREQUENCY=5

# Command to run the application using Python
CMD ["python", "syncatron.py"]