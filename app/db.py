from typing import Annotated
from sqlmodel import Session, create_engine, SQLModel
from fastapi import Depends, FastAPI
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sqlite_name = "db.sqlite3"
sqlite_url = f"sqlite:///{BASE_DIR / sqlite_name}" # URL de la base de datos 
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_all_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]