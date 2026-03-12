FROM python:3.13-slim
WORKDIR /app
RUN useradd -ms /bin/bash appuser
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
USER appuser
EXPOSE 5040
CMD ["python", "main.py"]