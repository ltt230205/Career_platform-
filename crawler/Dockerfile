FROM python:3.10-slim

USER root

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir selenium

RUN pip install minio

RUN pip install webdriver-manager

WORKDIR /app

CMD ["python"]
