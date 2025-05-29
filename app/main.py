from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from app.schemas import (
    ReviewIn, TaskOut, SimilarOut
)
from app.config import DATABASE_URL
from app.models import Base, engine, get_db_session
from app.ml.embedder import embedder
from app.services.reviews import save_review
from app.tasks import find_similar_reviews

from pgvector.asyncpg import register_vector

app = FastAPI()


# Создание таблиц
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        await conn.run_sync(Base.metadata.create_all)


# Добавление отзыва
@app.post("/add_review")
async def add_review(payload: ReviewIn):
    emb = embedder.encode([payload.text])[0]
    review_id = await save_review(payload.text, payload.sentiment, emb)
    return {"id": review_id}


# Запуск поиска через Celery
@app.post("/find_similar", response_model=TaskOut)
def find_similar_endpoint(payload: ReviewIn):
    task = find_similar_reviews.delay(payload.text)
    return {"task_id": task.id}


# Проверка статуса
@app.get("/status/{task_id}", response_model=SimilarOut)
def get_status(task_id: str):
    result = find_similar_reviews.AsyncResult(task_id)
    if result.state == 'PENDING':
        return {"status": result.state}
    if result.state == 'SUCCESS':
        return {"status": result.state, "similar": result.result}
    return {"status": result.state, "info": str(result.info)}
