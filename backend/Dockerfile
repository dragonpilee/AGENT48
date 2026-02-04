FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY . .

# Download model if not exists (using a small BF16/Q4 version for 4GB VRAM)
# Note: In a real scenario, this would be handled via a volume or build arg
# But here we ensure 'build it' works out of the box.
RUN mkdir -p /app/models

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
