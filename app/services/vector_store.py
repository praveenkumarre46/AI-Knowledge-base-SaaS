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
        collection = Collection(COLLECTION_NAME)
    else:
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="org_id", dtype=DataType.INT64),
            FieldSchema(name="doc_id", dtype=DataType.INT64),
            FieldSchema(name="chunk_text", dtype=DataType.VARCHAR, max_length=2000),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),
        ]

        schema = CollectionSchema(fields)
        collection = Collection(name=COLLECTION_NAME, schema=schema)

    # 🔑 Ensure index exists (even if collection already existed)
    if not collection.has_index():
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {"nlist": 128}
        }
        collection.create_index(
            field_name="embedding",
            index_params=index_params
        )
        print("Milvus index created")

    return collection


def insert_embeddings(org_id, doc_id, chunks, embeddings):

    collection = Collection(COLLECTION_NAME)

    org_ids = [org_id] * len(chunks)
    doc_ids = [doc_id] * len(chunks)

    data = [
        org_ids,
        doc_ids,
        chunks,
        embeddings
    ]

    collection.insert(data)

    collection.flush()

    print("Embeddings + chunks stored in Milvus")


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