from sqlalchemy import select, distinct, func
from app.models import MovieReview, get_db_session
from typing import List


async def save_review(
    text: str,
    sentiment: int,
    embedding: list[float]
) -> int:
    async for session in get_db_session():
        review = MovieReview(
            text=text,
            sentiment=sentiment,
            embedding=embedding
        )
        session.add(review)
        await session.commit()
        await session.refresh(review)
        return review.id


async def find_similar(
    embedding: list[float],
    limit: int = 3
) -> List[str]:
    async for session in get_db_session():
        distance_expr = MovieReview.embedding.cosine_distance(embedding)
        dist_label = func.min(distance_expr).label("dist")
        stmt = (
            select(MovieReview.text, dist_label)
            .group_by(MovieReview.text)
            .order_by(dist_label)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return [row[0] for row in result.all()]
