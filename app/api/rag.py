from fastapi import APIRouter, Depends
from app.schemas.query import QueryRequest
from app.services.rag_service import rag_query
from app.core.security import get_current_user
from app.db import models

router = APIRouter(
    prefix="/rag",
    tags=["RAG"]
)


@router.post("/query")
def query_rag(
    req: QueryRequest,
    current_user: models.User = Depends(get_current_user)
):

    result = rag_query(
        req.question,
        current_user.org_id
    )

    return result