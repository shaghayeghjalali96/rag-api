from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import DocumentChunk
from app.services.ollama import create_embedding


def search_chunks(
    db: Session,
    question: str,
    top_k: int = 5,
) -> list[dict]:
    query_embedding = create_embedding(question)

    distance = DocumentChunk.embedding.cosine_distance(query_embedding)

    stmt = (
        select(
            DocumentChunk,
            distance.label("distance"),
        )
        .order_by(distance)
        .limit(top_k)
    )

    results = db.execute(stmt).all()

    return [
        {
            "content": chunk.content,
            "page_number": chunk.page_number,
            "filename": chunk.document.filename,
            "score": 1 - float(distance_value),
        }
        for chunk, distance_value in results
    ]
