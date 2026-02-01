FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Copy credentials (mount these as volumes in production)
# COPY credentials.json .
# COPY token.json .

ENV PYTHONUNBUFFERED=1

CMD ["python", "src/main.py"]
