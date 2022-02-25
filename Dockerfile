FROM python:3.9.7-slim

#File Author/Maintainer
MAINTAINER Mathemartins

ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]