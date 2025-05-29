from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs, async_sessionmaker, create_async_engine
)
from sqlalchemy import Column, Integer, Text
from pgvector.sqlalchemy import Vector
from .config import DATABASE_URL


engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session():
    async with async_session_maker() as session:
        yield session


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)


class MovieReview(Base):
    __tablename__ = 'movie_reviews'
    text = Column(Text, nullable=False)
    sentiment = Column(Integer)  # <- Здесь было бы логичнее реализовать Boolean так как в колонке используется 0/1 значения
    embedding = Column(Vector(768))
