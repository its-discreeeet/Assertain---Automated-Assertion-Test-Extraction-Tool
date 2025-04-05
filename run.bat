@echo off
echo Building Docker image...
docker build -t assertion-extractor .

echo Extracting assertions from Requests...
docker run -v %cd%:/app/output assertion-extractor https://github.com/psf/requests

echo Extracting assertions from Flask...
docker run -v %cd%:/app/output assertion-extractor https://github.com/pallets/flask

echo Extracting assertions from Django...
docker run -v %cd%:/app/output assertion-extractor https://github.com/django/django

echo Extraction complete. CSV files have been generated.