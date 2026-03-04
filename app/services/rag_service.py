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

        contexts.append({"text": text, "distance": hit.distance})

    return contexts