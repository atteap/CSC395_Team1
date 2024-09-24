FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["python3", "app.py"]
