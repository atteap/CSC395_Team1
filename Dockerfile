FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
EXPOSE 8000

ENV OLLAMA_API_URL="http://localhost:8000"

CMD ["python", "app.py"]
