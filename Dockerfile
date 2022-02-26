FROM python:3.9.7

#File Author/Maintainer
MAINTAINER Mathemartins

ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app
#RUN apk update && apk add python3-dev \
#                        gcc \
#                        libc-dev
RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh

CMD ["/app/entrypoint.sh"]