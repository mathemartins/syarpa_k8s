#!/bin/bash

APP_PORT=${PORT:-8000}
cd /app/
#/opt/venv/bin/gunicorn --worker-tmp-dir /dev/shm syarpa_k8s.wsgi:application --bind "0.0.0.0:${APP_PORT}"
/opt/venv/bin/daphne syarpa_k8s.asgi:application --port $PORT --bind 0.0.0.0 -v2 && /opt/venv/bin/celery -A syarpa_k8s worker -l INFO --concurrency 1 -P solo && /opt/venv/bin/celery -A syarpa_k8s beat -l INFO
