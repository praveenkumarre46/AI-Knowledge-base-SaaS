from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.dependencies import get_db
from app.db import models
from app.schemas.user import UserCreate, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if org exists
    org = db.query(models.Organization).filter_by(name=user.org_name).first()

    if not org:
        org = models.Organization(name=user.org_name)
        db.add(org)
        db.commit()
        db.refresh(org)

    # Check if user exists
    existing_user = db.query(models.User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)

    new_user = models.User(
        email=user.email,
        password=hashed_pw,
        org_id=org.id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({
        "user_id": user.id,
        "org_id": user.org_id
    })

    return {"access_token": access_token, "token_type": "bearer"}