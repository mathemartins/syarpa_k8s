#!/bin/bash

cd /app/
/opt/venv/bin/celery -A syarpa_k8s beat -l INFO