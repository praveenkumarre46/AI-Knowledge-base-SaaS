from fastapi import APIRouter, Depends

from app.schemas.query import QueryRequest
from app.services.rag_service import retrieve_context, answer_question
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

    # return both retrieved contexts and a generated answer from local LLM
    result = answer_question(
        question=req.question,
        org_id=current_user.org_id
    )

    return {
        "question": req.question,
        "answer": result.get("answer"),
        "retrieved_chunks": result.get("contexts")
    }