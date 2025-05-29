from celery import Celery

from app.config import CELERY_BROKER_URL

celery = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_BROKER_URL)


@celery.task
def find_similar_reviews(text: str):

    import asyncio
    from app.ml.embedder import embedder
    from app.services.reviews import find_similar

    emb = embedder.encode([text])[0]

    return asyncio.get_event_loop().run_until_complete(find_similar(emb))
