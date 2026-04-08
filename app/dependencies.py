import os
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from dotenv import load_dotenv
from .database import SessionLocal
# from . import models

load_dotenv()

