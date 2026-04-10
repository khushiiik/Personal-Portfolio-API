import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from dotenv import load_dotenv
from app import models, schemas
from app.dependencies import get_db

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Route 1: User registration.
@router.post("/register", response_model=schemas.user.UserResponse, status_code=201)
def register(user: schemas.user.UserCreate, db: Session = Depends(get_db)):

    # Check if email already registered.
    existing = (
        db.query(models.user.User).filter(models.user.User.email == user.email).first()
    )
    if existing:
        raise HTTPException(400, "Email already registered!")

    # Hash the password.
    hashed_pwd = pwd_context.hash(user.password)

    # Create SQLAlchemy User object
    db_user = models.user.User(
        name=user.name, email=user.email, hashed_password=hashed_pwd
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# Route 2: User login.
@router.post("/login", response_model=schemas.user.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    # Find user by email.
    user_email = (
        db.query(models.user.User)
        .filter(models.user.User.email == form.username)
        .first()
    )

    # Verify password
    if not user_email or not pwd_context.verify(
        form.password, user_email.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expiry = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_email.email, "exp": expiry, "role": user_email.role}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}

