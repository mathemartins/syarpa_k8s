from django.conf.global_settings import TIME_ZONE

uri = "rediss://default:KCAnYINTOypslB2a@private-db-redis-redis-do-user-10904361-0.b.db.ondigitalocean.com:25061"

# Celery Settings
CELERY_BROKER_URL = uri
CELERY_RESULT_BACKEND = "django-db"
BROKER_POOL_LIMIT = None
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE