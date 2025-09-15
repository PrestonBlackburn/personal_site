FROM python:3.10-slim

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTESCODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /

COPY app/ /app
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["uvicorn", "app.host:app", "--proxy-headers", "--forwarded-allow-ips=*", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]
# uvicorn app.host:app --proxy-headers --forwarded-allow-ips="*" --host 0.0.0.0 --port 8000 --log-level debug
# uvicorn app.host:app --host 0.0.0.0 --port 8001
# test prompt: What are some details about the technical writing course? Your response should be 2000 words

# docker build . -t personal_site:latest
# docker run --rm -p 8000:8000 --name personal_site personal_site:latest 