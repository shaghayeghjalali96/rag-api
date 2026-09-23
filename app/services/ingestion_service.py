import json

from sqlalchemy.orm import Session

from app.ingestion.chunker import chunk_text
from app.ingestion.pdf import extract_pdf_pages
from app.models.document import Document, DocumentChunk
from app.services.ollama import create_embedding


def ingest_pdf(db: Session, file_path: str, filename: str) -> Document:
    pages = extract_pdf_pages(file_path)

    document = Document(
        filename=filename,
        metadata_json=json.dumps(
            {
                "source_type": "pdf",
                "filename": filename,
            }
        ),
    )

    db.add(document)
    db.flush()

    chunk_index = 0

    for page in pages:
        chunks = chunk_text(page["text"])

        for content in chunks:
            embedding = create_embedding(content)

            chunk = DocumentChunk(
                document_id=document.id,
                content=content,
                page_number=page["page_number"],
                chunk_index=chunk_index,
                embedding=embedding,
            )

            db.add(chunk)
            chunk_index += 1

    db.commit()
    db.refresh(document)

    return document
