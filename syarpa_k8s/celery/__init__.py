from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'syarpa_k8s.settings')

app = Celery('syarpa_k8s')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'get_coins_data_from_coingecko_30s': {'task': 'coins.tasks.get_coins_data_from_coingecko', 'schedule': 60.0},
}
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.CELERY_TIMEZONE = 'UTC'
app.autodiscover_tasks()

# web: daphne syarpa_k8s.asgi:application --port $PORT --bind 0.0.0.0 -v2
# worker: python manage.py runworker --settings=syarpa_k8s.settings -v2

# celery -A syarpa_k8s worker -l INFO --concurrency 1 -P solo
# celery -A syarpa_k8s beat -l INFO
