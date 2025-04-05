FROM python:3.9-slim

WORKDIR /app

# Install git and other dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install required Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the assertion extractor
COPY assertion_extractor.py .

# Make the script executable
RUN chmod +x assertion_extractor.py

# Set the entry point
ENTRYPOINT ["python", "assertion_extractor.py"]

# Default command (can be overridden)
CMD ["https://github.com/requests/requests"]