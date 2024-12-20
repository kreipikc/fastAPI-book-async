FROM python:3.9-slim

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

WORKDIR /api

COPY . /api
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR ../

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
