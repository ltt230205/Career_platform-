FROM python:3.10-slim

USER root

# 1. Cài Chromium + thư viện cần thiết
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

# 2. Cài Selenium
RUN pip install --no-cache-dir selenium

# 3. Set working dir
WORKDIR /app

CMD ["python"]
