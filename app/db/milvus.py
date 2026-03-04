from pymilvus import connections


def connect_milvus():
    connections.connect(
        alias="default",
        host="localhost",
        port="19530"
    )
    print("Milvus connected")