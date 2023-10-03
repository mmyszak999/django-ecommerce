FROM python:3.11.0-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get install -y libmagic-dev \
    && apt-get install make

COPY requirements.txt .

RUN pip install -r /app/requirements.txt \
    && pip install psycopg2

COPY . .

ENTRYPOINT ["python3", "manage.py", "runserver", "0.0.0.0:8000"]