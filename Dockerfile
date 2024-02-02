FROM python:3.12-slim-buster

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --no-cache-dir flask

CMD ["python", "/app/main.py"]
