#!/bin/bash

# Build the Docker image
echo "Building Docker image..."
docker build -t assertion-tool .

# Run the Docker container
echo "Running Docker container..."
docker run --rm assertion-tool