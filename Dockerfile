FROM python:3.9-slim

# Install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set up your application
WORKDIR /app
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code to the container
COPY ./src /app

# Command to run your Flask app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--timeout", "0", "app:app"]
