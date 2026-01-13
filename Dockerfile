# Use Python 3.10 base image
FROM python:3.10-slim

# Set Working Directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libstdc++6 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of application code
COPY . .

# Expose the application port
EXPOSE 8000

# Command to start FASTAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]