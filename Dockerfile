FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY code/assertion_extractor.py code/

ENTRYPOINT ["python", "code/assertion_extractor.py"]

# i have chosen this URL as an example, you can change it to any other URL you want like flask, django etc,
CMD ["https://github.com/requests/requests"]