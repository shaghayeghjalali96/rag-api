# Production RAG API

A production-oriented Retrieval-Augmented Generation API built from the fundamentals.

## Architecture

PDF
-> Text Extraction
-> Chunking
-> Embeddings
-> PostgreSQL + pgvector
-> Similarity Search
-> LLM
-> Answer + Sources

## Week 1 Stack

- Python
- FastAPI
- PostgreSQL
- pgvector
- Ollama
- Docker
- pypdf

## Run

### 1. Start PostgreSQL

```bash
docker compose up -d
```

### 2. Install Python dependencies

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Install Ollama models

```bash
ollama pull nomic-embed-text
ollama pull llama3.1:8b
```

If your local LLM has a different name, update `LLM_MODEL` in `.env`.

### 4. Create environment file

Copy:

```text
.env.example
```

to:

```text
.env
```

### 5. Run API

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## First test

Use `/documents/ingest` to upload a PDF.

Then use `/query`:

```json
{
  "question": "What is the main idea of this document?"
}
```

## Roadmap

- Week 1: basic RAG pipeline
- Week 2: hybrid retrieval + reranking
- Week 3: evaluation + streaming + caching + tests
- Later: observability, deployment, Kubernetes
