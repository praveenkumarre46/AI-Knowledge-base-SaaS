from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.db import models
from app.schemas.document import DocumentCreate
from app.core.security import get_current_user
from app.services.rag_service import process_document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Upload document + process RAG
@router.post("/")
def upload_document(
    doc: DocumentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    new_doc = models.Document(
        title=doc.title,
        content=doc.content,
        org_id=current_user.org_id,
        uploaded_by=current_user.id
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # RAG ingestion
    chunks = process_document(
        org_id=current_user.org_id,
        doc_id=new_doc.id,
        text=doc.content
    )

    return {
        "message": "Document uploaded",
        "chunks_created": chunks
    }


# List documents
@router.get("/")
def list_documents(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    docs = db.query(models.Document).filter(
        models.Document.org_id == current_user.org_id
    ).all()

    return docs