FROM python:3.11.11-slim

COPY pyairbyte/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /pyairbyte
COPY pyairbyte/main.py .
CMD ["python3", "main.py"]
