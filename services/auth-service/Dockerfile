FROM python:3.11-slim

WORKDIR /app

COPY ./src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi"]
