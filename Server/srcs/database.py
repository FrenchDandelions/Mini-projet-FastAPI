from sqlmodel import create_engine, Session, SQLModel
from contextlib import asynccontextmanager
from fastapi import FastAPI
import os


sqlite_file_name = os.environ["DATABASE"]
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def init_db():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Provide a database session."""
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database when the app starts."""
    init_db()
    yield
