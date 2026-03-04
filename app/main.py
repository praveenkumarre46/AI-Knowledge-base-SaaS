from fastapi import FastAPI

from app.db.database import engine
from app.db import models

from app.api import auth
from app.api import documents
from app.api import rag

from app.db.milvus import connect_milvus
from app.services.vector_store import create_collection


# Create database tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.on_event("startup")
def startup_event():
    connect_milvus()
    create_collection()


app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(rag.router)