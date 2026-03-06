FROM python:3.13-slim

WORKDIR /app

RUN useradd -m appuser \
    && mkdir -p /app/instance \
    && chown -R appuser:appuser /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

EXPOSE 5020

CMD ["python", "wsgi.py"]