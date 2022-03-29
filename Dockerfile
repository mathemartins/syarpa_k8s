FROM python:3.9.7

#File Author/Maintainer
MAINTAINER Mathemartins

ENV PYTHONUNBUFFERED 1

COPY . /app
WORKDIR /app

# supervisor installation &&
# create directory for child images to store configuration in
#RUN apt-get -y install supervisor && \
#  mkdir -p /var/log/supervisor && \
#  mkdir -p /etc/supervisor/conf.d


RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install pip --upgrade && \
    /opt/venv/bin/pip install -r requirements.txt && \
    chmod +x entrypoint.sh


# supervisor base configuration
#ADD supervisor.conf /etc/supervisor.conf

# default command
#CMD ["supervisord", "-c", "/etc/supervisor.conf"]

CMD ["/app/entrypoint.sh"]