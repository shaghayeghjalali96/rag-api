import requests

from app.core.config import settings


def create_embedding(text: str) -> list[float]:
    response = requests.post(
        f"{settings.ollama_url}/api/embed",
        json={
            "model": settings.embedding_model,
            "input": text,
        },
        timeout=120,
    )
    response.raise_for_status()

    data = response.json()
    return data["embeddings"][0]


def generate_answer(question: str, contexts: list[dict]) -> str:
    context_text = "\n\n".join(
        [
            f"[Source {i + 1} | {item['filename']} | page {item['page_number']}]\n"
            f"{item['content']}"
            for i, item in enumerate(contexts)
        ]
    )

    prompt = f"""
You are a helpful question-answering assistant.

Answer the user's question using ONLY the provided context.
If the context does not contain enough information, say that you do not
have enough information.

Always cite the source number you used, for example [Source 1].

Context:
{context_text}

Question:
{question}
""".strip()

    response = requests.post(
        f"{settings.ollama_url}/api/chat",
        json={
            "model": settings.llm_model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "stream": False,
        },
        timeout=180,
    )
    response.raise_for_status()

    return response.json()["message"]["content"]
