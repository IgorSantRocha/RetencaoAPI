from typing import Generator
from fastapi.security import OAuth2PasswordBearer
from core.config import settings
from db.session import SessionLocal, SessionLocal_211


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_db_211() -> Generator:
    try:
        db = SessionLocal_211()
        yield db
    finally:
        db.close()
