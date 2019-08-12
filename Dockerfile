FROM docker.io/library/python:rc-slim-buster
LABEL maintainer="ZeroExistence"

RUN useradd -m -d /app -u 44440 python

VOLUME ["/data"]

COPY --chown=44440 . /app/

RUN apt-get update && apt-get --no-install-recommends -y install gcc libjpeg62-turbo-dev zlib1g-dev && pip3 --no-cache-dir install -r /app/requirements.txt && apt-get clean && rm -rf /var/lib/apt/lists/* && rm -rf ~/.cache/pip && chown -Rv 44440 /data

USER 44440

CMD ["uwsgi","--ini","/app/uwsgi.ini"]
