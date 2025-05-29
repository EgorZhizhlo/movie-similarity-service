from pydantic import BaseModel


class ReviewIn(BaseModel):
    text: str
    sentiment: int


class TaskOut(BaseModel):
    task_id: str


class SimilarOut(BaseModel):
    status: str
    similar: list[str] | None = None
    info: str | None = None
