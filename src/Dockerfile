FROM python:3.10-slim-buster

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN apt-get update && apt-get install gcc libcurl4-openssl-dev libssl-dev -y

RUN apt-get update && apt-get install default-libmysqlclient-dev -y

RUN cd /app/ && poetry install

EXPOSE 8000:8000

COPY moodtracker /app/moodtracker
COPY treatment /app/treatment
COPY manage.py /app/manage.py
COPY patient /app/patient
COPY tracker /app/tracker

# figure out how to conditionally copy these
COPY frontend_build/index.html /app/frontend_build/index.html
COPY frontend_build/static/ /app/frontend_build/static

ENV DJANGO_SETTINGS_MODULE=moodtracker.settings

COPY supervisor /etc/supervisor/

RUN touch /var/log/gunicorn.log && touch /var/log/gunicorn_err.log
RUN touch /var/log/celery.log && touch /var/log/celery_err.log
RUN touch /var/log/celery_beat.log && touch /var/log/celery_beat_err.log

RUN pip install supervisor

ENV PYTHONUNBUFFERED=1

ENTRYPOINT supervisord -c /etc/supervisor/supervisord.conf --nodaemon "$@"
