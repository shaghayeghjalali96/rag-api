from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)


class Source(BaseModel):
    filename: str
    page_number: int | None
    score: float
    content: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[Source]
