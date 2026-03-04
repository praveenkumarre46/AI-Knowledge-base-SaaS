from fastapi import FastAPI
from app.db.database import engine
from app.db import models
from app.api import auth

app = FastAPI(title="AI Knowledge Base SaaS")

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Backend running 🚀"}

from app.core.security import get_current_user
from app.db import models
from fastapi import Depends


@app.get("/protected")
def protected_route(current_user: models.User = Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user_id": current_user.id,
        "org_id": current_user.org_id
    }