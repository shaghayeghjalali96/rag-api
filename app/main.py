import os
import tempfile

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import Base, engine, get_db
from app.models import Document, DocumentChunk
from app.schemas import QueryRequest, QueryResponse, Source
from app.services.ingestion_service import ingest_pdf
from app.services.ollama import generate_answer
from app.services.retrieval import search_chunks


# Import models before create_all.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Production RAG API",
    version="0.1.0",
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/documents/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    suffix = ".pdf"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        temp_path = tmp.name

    try:
        document = ingest_pdf(
            db=db,
            file_path=temp_path,
            filename=file.filename,
        )

        return {
            "id": document.id,
            "filename": document.filename,
            "message": "Document ingested successfully.",
        }

    finally:
        os.unlink(temp_path)


@app.post("/query", response_model=QueryResponse)
def query(
    request: QueryRequest,
    db: Session = Depends(get_db),
):
    chunks = search_chunks(
        db=db,
        question=request.question,
        top_k=5,
    )

    if not chunks:
        raise HTTPException(
            status_code=404,
            detail="No documents have been indexed yet.",
        )

    answer = generate_answer(
        question=request.question,
        contexts=chunks,
    )

    return QueryResponse(
        answer=answer,
        sources=[
            Source(**chunk)
            for chunk in chunks
        ],
    )
