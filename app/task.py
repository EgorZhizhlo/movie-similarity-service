from celery import Celery
import asyncio

from app.config import CELERY_BROKER_URL
from app.ml.embedder import Embedder
from app.services.reviews import find_similar

celery = Celery('tasks', broker=CELERY_BROKER_URL)
embedder = Embedder(model_dir='models/distilbert-imdb')


@celery.task
def find_similar_reviews(text: str):
    emb = embedder.encode([text])[0]
    return asyncio.get_event_loop().run_until_complete(
        find_similar(emb)
    )
