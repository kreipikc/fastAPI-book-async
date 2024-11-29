FROM python:3.9-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

COPY . /app

WORKDIR ../

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
