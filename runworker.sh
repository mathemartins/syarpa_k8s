#!/bin/bash
cd /app/

/opt/venv/bin/celery -A syarpa_k8s worker -l INFO --concurrency 1 -P solo