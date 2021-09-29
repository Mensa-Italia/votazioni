# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /srv
COPY requirements.txt /srv/
RUN pip install -r requirements.txt
COPY . /srv/