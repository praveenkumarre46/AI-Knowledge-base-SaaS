from pymilvus import (
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
    utility
)

COLLECTION_NAME = "document_chunks"


def create_collection():

    if utility.has_collection(COLLECTION_NAME):
        print("Collection already exists")
        return Collection(COLLECTION_NAME)

    fields = [

        FieldSchema(
            name="id",
            dtype=DataType.INT64,
            is_primary=True,
            auto_id=True
        ),

        FieldSchema(
            name="org_id",
            dtype=DataType.INT64
        ),

        FieldSchema(
            name="doc_id",
            dtype=DataType.INT64
        ),

        FieldSchema(
            name="chunk_text",
            dtype=DataType.VARCHAR,
            max_length=2048
        ),

        FieldSchema(
            name="embedding",
            dtype=DataType.FLOAT_VECTOR,
            dim=384
        )

    ]

    schema = CollectionSchema(fields)

    collection = Collection(
        name=COLLECTION_NAME,
        schema=schema
    )

    print("Collection created")

    # create index for faster search
    try:
        from pymilvus import Index

        index_params = {
            "index_type": "HNSW",
            "metric_type": "L2",
            "params": {"M": 16, "efConstruction": 200}
        }

        Index(collection, "embedding", index_params)
        print("Index created for embedding")
    except Exception:
        print("Failed to create index (it may already exist)")

    # load collection for search/insert
    collection.load()

    return collection
from pymilvus import Collection

COLLECTION_NAME = "document_chunks"


def insert_embeddings(org_id, doc_id, embeddings, chunk_texts=None):

    collection = Collection(COLLECTION_NAME)

    org_ids = [org_id] * len(embeddings)
    doc_ids = [doc_id] * len(embeddings)

    if chunk_texts is None:
        chunk_texts = [""] * len(embeddings)

    data = [
        org_ids,
        doc_ids,
        chunk_texts,
        embeddings
    ]

    collection.insert(data)

    collection.flush()

    print("Embeddings inserted into Milvus")
from pymilvus import Collection

COLLECTION_NAME = "document_chunks"

def search_embeddings(query_embedding, org_id, top_k=5):

    collection = Collection(COLLECTION_NAME)

    collection.load()

    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=top_k,
        expr=f"org_id == {org_id}",
        output_fields=["chunk_text", "doc_id"]
    )

    return results