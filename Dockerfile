# syntax=docker/dockerfile:1
FROM tiangolo/uvicorn-gunicorn:python3.9
ENV PYTHONUNBUFFERED=1
WORKDIR /srv
COPY requirements.txt /srv/
RUN pip install -r requirements.txt
COPY . /srv/
cmd 'run.sh'
