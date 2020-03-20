FROM python:3.7
MAINTAINER https://github.com/nevidanniu/

ENV FLASK_APP promenad.py

RUN apt-get update && apt-get install -y \
    curl tzdata libpq-dev \
    && apt-get clean

ENV TZ=Europe/Moscow

RUN adduser --disabled-password --gecos "" promenad
WORKDIR /home/promenad

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt && pip3 install gunicorn

COPY config.py ConsulClient.py promenad.py ./
COPY app app
RUN chown -R promenad:promenad ./

ENV SECRET_KEY sldsakjsas
ENV CONSUL_PORT 8500
USER promenad

EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/gunicorn", "-t", "120", "-w", "1", "--error-logfile", "-", "--access-logfile", "-", "-b", ":8000", "promenad:app"]
