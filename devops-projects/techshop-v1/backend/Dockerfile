FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN groupadd -r myuser && useradd -r -g myuser -u 1000 -m myuser
RUN chown -R myuser:myuser /app
USER myuser
EXPOSE 5000
CMD ["gunicorn -w 4 -b 0.0.0.0:5000 app:app"]