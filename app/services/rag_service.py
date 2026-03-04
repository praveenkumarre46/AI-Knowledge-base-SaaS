from app.services.vector_store import search_embeddings
from app.services.llm_service import generate_answer
from app.utils.chunking import chunk_text
from app.services.embedding_service import generate_embedding
from app.services.vector_store import insert_embeddings


def process_document(org_id: int, doc_id: int, text: str):

    chunks = chunk_text(text)

    embeddings = []

    for chunk in chunks:
        emb = generate_embedding(chunk)
        embeddings.append(emb)

    insert_embeddings(
    org_id,
    doc_id,
    chunks,
    embeddings
)

    return len(chunks)


def retrieve_context(question: str, org_id: int):

    query_embedding = generate_embedding(question)

    results = search_embeddings(query_embedding, org_id)

    contexts = []

    for hit in results[0]:
        contexts.append(hit.entity.get("chunk_text"))

    return contexts


def answer_question(question: str, org_id: int, model: str = "llama2"):
    """Retrieve context and call local LLM (Ollama) to generate an answer.

    Returns a dict with the answer text and the retrieved contexts used.
    """
    contexts = retrieve_context(question, org_id)

    # build prompt
    prompt_lines = [
        "You are an assistant that answers user questions using the provided context snippets.",
        "If the answer is not contained in the context, reply with 'I don't know'.",
        "\nContext snippets:\n"
    ]

    for i, c in enumerate(contexts, start=1):
        snippet = c.get("text") or ""
        prompt_lines.append(f"[{i}] {snippet}\n")

    prompt_lines.append("\nQuestion:\n")
    prompt_lines.append(question)
    prompt_lines.append("\n\nAnswer:")

    prompt = "\n".join(prompt_lines)

    llm_result = generate_answer(question, contexts)

    return {"answer": llm_result, "contexts": contexts}
from app.services.llm_service import generate_answer


def rag_query(question: str, org_id: int):

    contexts = retrieve_context(question, org_id)

    answer = generate_answer(question, contexts)

    return {
        "answer": answer,
        "sources": contexts
    }