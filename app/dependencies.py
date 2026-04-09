import os
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from dotenv import load_dotenv
from .database import SessionLocal
from app.models import user

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


# Dependency 1: db session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency 2: Validate user.
def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> user.User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_error
    except JWTError:
        raise credentials_error

    user_email = db.query(user.User).filter(user.User.email == email).first()
    if user_email is None:
        raise credentials_error

    if not user_email.is_active:
        raise HTTPException(400, "Inactive user!")

    return user_email
