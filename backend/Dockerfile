FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && pip install -r requirements.txt

COPY . ./

CMD gunicorn --bind 0.0.0.0:8080 foodgram.wsgi:application
