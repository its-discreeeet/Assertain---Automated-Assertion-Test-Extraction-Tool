# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install Git and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the assertion extractor script
COPY code/assertion_extractor.py code/

# Set the entry point to run the script
ENTRYPOINT ["python", "code/assertion_extractor.py"]

# Provide a default GitHub repository URL
CMD ["https://github.com/requests/requests"]