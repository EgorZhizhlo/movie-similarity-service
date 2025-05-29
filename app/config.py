import os

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
DATABASE_URL = os.environ.get('DATABASE_URL')
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')

if not DATABASE_URL or not CELERY_BROKER_URL:
    raise RuntimeError(
        "DATABASE_URL или CELERY_BROKER_URL не заданы в окружении")
