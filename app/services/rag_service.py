from app.utils.chunking import chunk_text
from app.services.embedding_service import generate_embedding
from app.services.vector_store import insert_embeddings


def process_document(org_id: int, doc_id: int, text: str):

    # Step 1: Chunk text
    chunks = chunk_text(text)

    embeddings = []
    chunk_texts = []

    # Step 2: Generate embeddings
    for chunk in chunks:
        emb = generate_embedding(chunk)
        embeddings.append(emb)
        chunk_texts.append(chunk)

    # Step 3: Store in Milvus
    insert_embeddings(org_id, doc_id, embeddings, chunk_texts=chunk_texts)

    return len(chunks)
from app.services.embedding_service import generate_embedding
from app.services.vector_store import search_embeddings
from app.services.llm_service import call_ollama

def retrieve_context(question: str, org_id: int):

    # generate query embedding
    query_embedding = generate_embedding(question)

    # search Milvus
    results = search_embeddings(query_embedding, org_id)

    contexts = []

    for hit in results[0]:
        # hit.entity contains returned fields when output_fields specified
        text = None
        try:
            text = hit.entity.get("chunk_text")
        except Exception:
            # fallback: empty
            text = ""

        doc_id = None
        try:
            doc_id = hit.entity.get("doc_id")
        except Exception:
            doc_id = None

        contexts.append({"text": text, "distance": hit.distance, "doc_id": doc_id})

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

    llm_result = call_ollama(prompt, model=model)

    return {"answer": llm_result, "contexts": contexts}