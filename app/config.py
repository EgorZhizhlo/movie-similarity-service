import os

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
DATABASE_URL = os.getenv('DATABASE_URL')
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')

if not DATABASE_URL or not CELERY_BROKER_URL:
    raise RuntimeError(
        "DATABASE_URL или CELERY_BROKER_URL не заданы в окружении")
